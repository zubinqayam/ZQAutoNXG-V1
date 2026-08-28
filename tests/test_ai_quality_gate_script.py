import importlib.util
import json
from pathlib import Path
from urllib.parse import urlparse


SCRIPT_PATH = Path(__file__).resolve().parents[1] / ".github" / "scripts" / "run_ai_quality_gate.py"
SPEC = importlib.util.spec_from_file_location("run_ai_quality_gate", SCRIPT_PATH)
assert SPEC and SPEC.loader
run_ai_quality_gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(run_ai_quality_gate)


class _FakeHTTPResponse:
    def __init__(self, payload: dict):
        self._payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def read(self):
        return json.dumps(self._payload).encode("utf-8")


def test_call_gemini_returns_joined_text_parts(monkeypatch):
    def _fake_urlopen(request, timeout=45):  # noqa: ARG001
        parsed_url = urlparse(request.full_url)
        assert parsed_url.netloc == "generativelanguage.googleapis.com"
        assert parsed_url.path.endswith(":generateContent")
        assert parsed_url.query == "key=test-key"
        return _FakeHTTPResponse(
            {
                "candidates": [
                    {
                        "content": {
                            "parts": [
                                {"text": "HIGH: foo.py:10 — issue — why — fix"},
                                {"text": "LOW: bar.py:5 — issue — why — fix"},
                            ]
                        }
                    }
                ]
            }
        )

    monkeypatch.setattr(run_ai_quality_gate.urllib.request, "urlopen", _fake_urlopen)

    findings = run_ai_quality_gate.call_gemini("system", "user", "test-key")
    assert findings == (
        "HIGH: foo.py:10 — issue — why — fix\n"
        "LOW: bar.py:5 — issue — why — fix"
    )


def test_main_skips_without_gemini_api_key(tmp_path, monkeypatch):
    diff_file = tmp_path / "scoped.diff"
    policy_file = tmp_path / "policy.yml"
    prompt_file = tmp_path / "prompt.md"
    output_file = tmp_path / "out.md"
    diff_file.write_text("diff --git a/a.py b/a.py\n", encoding="utf-8")
    policy_file.write_text("checks: {}\n", encoding="utf-8")
    prompt_file.write_text("prompt", encoding="utf-8")

    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.setattr(
        run_ai_quality_gate.sys,
        "argv",
        [
            "run_ai_quality_gate.py",
            "--diff",
            str(diff_file),
            "--policy",
            str(policy_file),
            "--prompt",
            str(prompt_file),
            "--output",
            str(output_file),
        ],
    )

    assert run_ai_quality_gate.main() == 0
    assert output_file.read_text(encoding="utf-8").strip() == "AI review skipped: no API key configured."
