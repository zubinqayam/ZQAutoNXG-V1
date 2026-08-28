#!/usr/bin/env python3
"""AI Quality Gate runner.

Sends a filtered, secret-redacted diff plus the repository policy and
review prompt to the Gemini API, then writes the structured findings to an
output file consumed by the GitHub Actions workflow.

API key must be supplied via the GEMINI_API_KEY environment variable,
sourced from a GitHub Actions secret. This script never logs or persists
the key.
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

SECRET_ASSIGNMENT = re.compile(
    r"(?im)\b(?P<key>[A-Z0-9_.-]*(?:API[_-]?KEY|SECRET|TOKEN|PASSWORD|PASSWD|PWD)[A-Z0-9_.-]*)"
    r"\s*(?P<sep>[:=])\s*(?P<quote>['\"]?)(?P<value>[^\s,'\"}\]]{8,})(?P=quote)"
)
CONNECTION_CREDENTIALS = re.compile(
    r"(?i)\b(?P<scheme>postgres(?:ql)?|mysql|mariadb|redis|mongodb(?:\+srv)?):\/\/"
    r"(?P<credentials>[^@\s]+)@"
)
BEARER_TOKEN = re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]{12,}")
PRIVATE_KEY = re.compile(
    r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----.*?-----END [A-Z0-9 ]*PRIVATE KEY-----",
    re.DOTALL,
)
TOKEN_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}"),
]


def redact(text: str) -> str:
    """Mask common quoted/unquoted secrets before any external AI call."""
    text = SECRET_ASSIGNMENT.sub(
        lambda match: f"{match.group('key')}{match.group('sep')}[REDACTED-SECRET]",
        text,
    )
    text = CONNECTION_CREDENTIALS.sub(
        lambda match: f"{match.group('scheme')}://[REDACTED-CREDENTIALS]@",
        text,
    )
    text = BEARER_TOKEN.sub("Bearer [REDACTED-SECRET]", text)
    text = PRIVATE_KEY.sub("[REDACTED-PRIVATE-KEY]", text)
    for pattern in TOKEN_PATTERNS:
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

    api_key = os.environ.get("GEMINI_API_KEY")
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
        findings = call_gemini(system_prompt, user_prompt, api_key)
    except Exception as exc:  # noqa: BLE001
        findings = f"AI review failed to run: {type(exc).__name__}. See workflow logs."

    with open(args.output, "w", encoding="utf-8") as fh:
        fh.write(findings.strip() + "\n")

    return 0


def call_gemini(system_prompt: str, user_prompt: str, api_key: str) -> str:
    """Call the Gemini REST API."""
    model = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")
    endpoint = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{urllib.parse.quote(model)}:generateContent?key={urllib.parse.quote(api_key)}"
    )
    payload = {
        "systemInstruction": {
            "parts": [
                {
                    "text": system_prompt,
                }
            ]
        },
        "contents": [
            {
                "parts": [
                    {
                        "text": user_prompt,
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0,
        },
    }
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        endpoint,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=45) as response:  # noqa: S310
            response_data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        response_body = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Gemini HTTP error {exc.code}: {response_body[:500]}") from exc

    candidates = response_data.get("candidates") or []
    if not candidates:
        return "No findings returned."

    parts = ((candidates[0].get("content") or {}).get("parts") or [])
    text_parts = [
        part.get("text", "")
        for part in parts
        if isinstance(part, dict) and part.get("text")
    ]
    findings = "\n".join(text_parts).strip()
    return findings or "No findings returned."


if __name__ == "__main__":
    sys.exit(main())
