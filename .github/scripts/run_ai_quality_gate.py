#!/usr/bin/env python3
"""AI Quality Gate runner.

Reads a filtered PR diff, redacts secret-like patterns, then calls the
Anthropic API with the review prompt and policy config.  Writes structured
findings to FINDINGS_PATH as JSON (including a ``markdown_comment`` field
suitable for posting as a GitHub PR comment) and exits non-zero when
CRITICAL findings are present.

Environment variables (all required):
    ANTHROPIC_API_KEY  – Populated from the GitHub Actions secret of the
                         same name.  Never hardcoded, never echoed.
    DIFF_PATH          – Path to the filtered diff file.
    POLICY_PATH        – Path to .github/ai-quality-gate.yml
    PROMPT_PATH        – Path to .github/ai-review-prompt.md
    FINDINGS_PATH      – Path where findings JSON is written.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

import anthropic
import yaml


# ---------------------------------------------------------------------------
# Secret-like pattern redaction
# ---------------------------------------------------------------------------

_SECRET_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("API_KEY", re.compile(
        r'(?i)(api[_\-]?key|apikey)\s*[:=]\s*["\']?([A-Za-z0-9_\-\.]{16,})["\']?'
    )),
    ("TOKEN", re.compile(
        r'(?i)(token|secret|password|passwd|pwd)\s*[:=]\s*["\']?([A-Za-z0-9_\-\.\/+]{16,})["\']?'
    )),
    ("PRIVATE_KEY_BLOCK", re.compile(
        r'-----BEGIN [A-Z ]+PRIVATE KEY-----[\s\S]*?-----END [A-Z ]+PRIVATE KEY-----'
    )),
    ("CONNECTION_STRING", re.compile(
        r'(?i)(postgres|mysql|mongodb|redis|amqp)://[^\s"\'<>]+'
    )),
    ("BEARER_TOKEN", re.compile(
        r'(?i)bearer\s+([A-Za-z0-9_\-\.\/+]{20,})'
    )),
    ("ANTHROPIC_KEY", re.compile(
        r'sk-ant-[A-Za-z0-9_\-]{20,}'
    )),
    ("OPENAI_KEY", re.compile(
        r'sk-[A-Za-z0-9]{20,}'
    )),
    ("GENERIC_SECRET", re.compile(
        r'(?i)(secret|credential)[_\-]?[a-z0-9]*\s*[:=]\s*["\']?([A-Za-z0-9_\-\.]{16,})["\']?'
    )),
]


def redact_diff(diff_text: str) -> str:
    """Replace secret-like patterns in *diff_text* with redaction markers."""
    redacted = diff_text
    for label, pattern in _SECRET_PATTERNS:
        def _replace(m: re.Match[str], lbl: str = label) -> str:  # noqa: ANN001
            return f"[REDACTED {lbl}]"
        redacted = pattern.sub(_replace, redacted)
    return redacted


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

MAX_DIFF_CHARS = 60_000  # stay well within model context limits


def _load_env(name: str) -> str:
    value = os.environ.get(name, "")
    if not value:
        print(f"::error::Required environment variable {name!r} is not set.", file=sys.stderr)
        sys.exit(1)
    return value


def _build_markdown_comment(findings_data: dict) -> str:
    """Render findings as a GitHub-flavoured Markdown PR comment."""
    lines: list[str] = [
        "## 🤖 AI Quality Gate Report",
        "",
        f"> **Summary:** {findings_data.get('summary', 'No summary provided.')}",
        "",
    ]
    findings: list[dict] = findings_data.get("findings", [])
    if not findings:
        lines.append("✅ No issues found by the AI Quality Gate reviewer.")
        return "\n".join(lines)

    severity_emoji = {
        "CRITICAL": "🚨",
        "HIGH": "🔴",
        "MEDIUM": "🟡",
        "LOW": "🔵",
    }

    current_severity = None
    for finding in findings:
        sev = finding.get("severity", "LOW")
        if sev != current_severity:
            current_severity = sev
            emoji = severity_emoji.get(sev, "ℹ️")
            lines.append(f"### {emoji} {sev}")
            lines.append("")

        file_ref = finding.get("file", "N/A")
        line_ref = finding.get("line", "N/A")
        check = finding.get("check", "")
        desc = finding.get("description", "")
        fix = finding.get("recommended_fix", "")

        lines.append(f"**[{check}]** `{file_ref}:{line_ref}`")
        lines.append(f"- **Issue:** {desc}")
        lines.append(f"- **Fix:** {fix}")
        lines.append("")

    if findings_data.get("has_critical"):
        lines.append("---")
        lines.append(
            "⛔ **This PR is blocked by CRITICAL findings above.** "
            "Resolve them before merging."
        )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    # --- Load required paths from environment ---
    api_key = _load_env("ANTHROPIC_API_KEY")
    diff_path = Path(_load_env("DIFF_PATH"))
    policy_path = Path(_load_env("POLICY_PATH"))
    prompt_path = Path(_load_env("PROMPT_PATH"))
    findings_path = Path(_load_env("FINDINGS_PATH"))

    # --- Read inputs ---
    if not diff_path.exists():
        print(f"::error::Diff file not found: {diff_path}", file=sys.stderr)
        sys.exit(1)
    diff_text = diff_path.read_text(encoding="utf-8", errors="replace")

    if not policy_path.exists():
        print(f"::error::Policy file not found: {policy_path}", file=sys.stderr)
        sys.exit(1)
    policy_raw = policy_path.read_text(encoding="utf-8")
    policy: dict = yaml.safe_load(policy_raw) or {}

    if not prompt_path.exists():
        print(f"::error::Prompt file not found: {prompt_path}", file=sys.stderr)
        sys.exit(1)
    system_prompt = prompt_path.read_text(encoding="utf-8")

    # --- Redact secrets from diff before sending to AI ---
    redacted_diff = redact_diff(diff_text)
    if len(redacted_diff) > MAX_DIFF_CHARS:
        redacted_diff = (
            redacted_diff[:MAX_DIFF_CHARS]
            + "\n\n[... diff truncated at 60,000 characters for safety ...]"
        )

    # --- Build model config from policy ---
    model_cfg: dict = policy.get("model", {})
    model_id: str = model_cfg.get("model_id", "claude-3-5-sonnet-20241022")
    max_tokens: int = int(model_cfg.get("max_tokens", 4096))
    temperature: float = float(model_cfg.get("temperature", 0))

    # --- Call Anthropic API ---
    client = anthropic.Anthropic(api_key=api_key)

    user_message = (
        "Below is the filtered pull-request diff to review.\n"
        "Apply every check described in your system instructions.\n"
        "Return only the JSON findings object — no other text.\n\n"
        "```diff\n"
        f"{redacted_diff}\n"
        "```"
    )

    print(f"Calling Anthropic API (model={model_id}, max_tokens={max_tokens}) …", flush=True)

    response = client.messages.create(
        model=model_id,
        max_tokens=max_tokens,
        temperature=temperature,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )

    raw_output: str = response.content[0].text if response.content else "{}"

    # --- Parse structured findings ---
    # Strip optional markdown code fences the model may add
    clean_output = raw_output.strip()
    if clean_output.startswith("```"):
        clean_output = re.sub(r"^```[a-z]*\n?", "", clean_output)
        clean_output = re.sub(r"\n?```$", "", clean_output)

    try:
        findings_data: dict = json.loads(clean_output)
    except json.JSONDecodeError as exc:
        print(
            f"::warning::Could not parse model JSON output: {exc}. "
            "Storing raw output and treating as non-critical.",
            file=sys.stderr,
        )
        findings_data = {
            "summary": "AI reviewer returned unparseable output.",
            "has_critical": False,
            "findings": [],
            "raw_output": raw_output[:2000],
        }

    # --- Attach markdown comment ---
    findings_data["markdown_comment"] = _build_markdown_comment(findings_data)

    # --- Write findings to disk ---
    findings_path.parent.mkdir(parents=True, exist_ok=True)
    findings_path.write_text(json.dumps(findings_data, indent=2), encoding="utf-8")
    print(f"Findings written to {findings_path}")

    # --- Exit code: non-zero if CRITICAL ---
    has_critical: bool = bool(findings_data.get("has_critical", False))
    if not has_critical:
        # Also check findings list directly in case model forgot the flag
        has_critical = any(
            f.get("severity") == "CRITICAL" for f in findings_data.get("findings", [])
        )

    if has_critical:
        print(
            "::error::AI Quality Gate found CRITICAL issues — PR is blocked. "
            "See PR comment for details.",
            file=sys.stderr,
        )
        sys.exit(1)

    print("AI Quality Gate review complete — no CRITICAL issues found.")


if __name__ == "__main__":
    main()
