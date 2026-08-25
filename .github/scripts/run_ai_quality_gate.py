#!/usr/bin/env python3
"""AI Quality Gate runner.

Sends a filtered, secret-redacted diff plus the repository policy and
review prompt to a single configured AI provider, then writes the
structured findings to an output file consumed by the GitHub Actions
workflow.

Provider is selected via AI_PROVIDER env var (default: openai).
API key must be supplied via the AI_API_KEY environment variable, sourced
from a GitHub Actions secret. This script never logs or persists the key.
"""
import argparse
import os
import re
import sys

SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"][^'\"]{8,}['\"]"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9]{30,}"),
    re.compile(r"ssh-(rsa|ed25519|ecdsa)[^\n]+"),
]


def redact(text: str) -> str:
    for pattern in SECRET_PATTERNS:
        text = pattern.sub("[REDACTED-SECRET]", text)
    return text


def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as fh:
        return fh.read()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--diff", required=True)
    parser.add_argument("--policy", required=True)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    api_key = os.environ.get("AI_API_KEY")
    if not api_key:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write("AI review skipped: no API key configured.\n")
        return 0

    diff_text = redact(read_file(args.diff))[:120_000]
    policy_text = read_file(args.policy)
    prompt_text = read_file(args.prompt)

    if not diff_text.strip():
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write("No relevant changes to review.\n")
        return 0

    system_prompt = prompt_text + "\n\n## Policy\n\n" + policy_text
    user_prompt = "## Filtered diff\n\n```diff\n" + diff_text + "\n```"

    try:
        findings = call_ai_provider(system_prompt, user_prompt, api_key)
    except Exception as exc:  # noqa: BLE001
        findings = f"AI review failed to run: {type(exc).__name__}. See workflow logs."

    with open(args.output, "w", encoding="utf-8") as fh:
        fh.write(findings.strip() + "\n")

    return 0


def call_ai_provider(system_prompt: str, user_prompt: str, api_key: str) -> str:
    """Call the configured AI provider. Import kept local so the script has
    no hard dependency when AI review is skipped."""
    provider = os.environ.get("AI_PROVIDER", "openai").lower()

    if provider == "openai":
        from openai import OpenAI  # type: ignore

        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=os.environ.get("AI_MODEL", "gpt-4.1-mini"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0,
        )
        return response.choices[0].message.content or "No findings returned."

    raise ValueError(f"Unsupported AI_PROVIDER: {provider}")


if __name__ == "__main__":
    sys.exit(main())
