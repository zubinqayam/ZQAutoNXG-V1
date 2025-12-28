# ZQAutoNXG - Copilot Instructions

## Overview
Python 3.11+ FastAPI application (~200 LOC) - REST API with Prometheus metrics. Architecture: G V2 NovaBase (hexagonal). License: Apache 2.0.

**Key Files**: `zqautonxg/app.py` (140 lines, FastAPI endpoints), `zqautonxg/__init__.py` (63 lines, metadata), `requirements.txt` (dependencies), `Dockerfile` (container build), `pyproject.toml` (package config), `deploy.sh` (deployment script).

**CI Workflows**: `.github/workflows/python-app.yml` (main CI: Python 3.10, flake8, pytest), `.github/workflows/release.yml` (security scans, Docker build, release).

**CRITICAL**: NO test files exist. pytest will fail due to pyproject.toml line 136 syntax error (nested quotes).

## Build & Run (ALWAYS in this order)

1. **Install dependencies** (~30-60s): `pip install -r requirements.txt`
2. **Run app**: `python3 -m uvicorn zqautonxg.app:app --reload --host 0.0.0.0 --port 8000`
   - Server starts on http://localhost:8000 (~2-3s)
   - Auto-reloads on changes (--reload flag)
3. **Test endpoints**:
   ```bash
   curl http://localhost:8000/        # Platform info
   curl http://localhost:8000/health  # Health check
   curl http://localhost:8000/metrics # Prometheus metrics
   ```

**Alternative**: `./deploy.sh dev` (includes venv setup and dependency installation)

## Linting & Testing

**Linting** (ALWAYS use `python3 -m` to avoid PATH issues):
```bash
pip install flake8
python3 -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics  # Critical errors
python3 -m flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics  # Warnings
```

**Testing**: NO test files exist. `pytest` fails with pyproject.toml syntax error (line 136, nested quotes in markers array).
- To add tests: Create `tests/` directory, install `pytest pytest-asyncio`, run `python3 -m pytest -v`

## Docker

**Build** (~2-3 min): `docker build -t zqautonxg:latest .` (Python 3.11-slim-bullseye)
**Run**: `docker run -d --name zqautonxg -p 8000:8000 zqautonxg:latest`
**Test** (wait 10s): `sleep 10 && curl http://localhost:8000/health`
**Script**: `./deploy.sh docker` (builds & runs with health checks)

## CI/CD Workflows

### python-app.yml (PR/main push, ~30-45s)
Steps: checkout → Python 3.10 setup → install deps (flake8, pytest, requirements.txt) → lint (flake8 2x) → **pytest (FAILS - see Known Issues)**

### release.yml (Tags/main/PRs, ~8-12 min)
Jobs: security-validation (Bandit, Safety, Ruff, MyPy) → build-and-test (multi-arch Docker → ghcr.io) → create-release (GitHub release) → summary

## Known Issues & Workarounds

1. **pytest fails in CI**: pyproject.toml line 136 has nested quotes: `"slow: marks tests as slow (deselect with '-m "not slow"')"`. Fix: escape or use single quotes: `'slow: marks tests as slow (deselect with "-m not slow")'`

2. **No tests exist**: CI runs pytest but no test files exist. Referenced CI failure (run #19844303584) is due to this + issue #1.

3. **Python version mismatch**: CI uses Python 3.10, repo requires 3.11+ (see `__init__.py` line 36). Update `python-app.yml` line 25 to `python-version: "3.11"`.

4. **Command not found**: After pip install, use `python3 -m flake8` not `flake8`, `python3 -m pytest` not `pytest`.

5. **Missing .gitignore**: No .gitignore exists. Add Python standard patterns to avoid committing `__pycache__/`.

## API Endpoints & Configuration

**Endpoints** (http://localhost:8000):
- `/` - Platform info, version, capabilities
- `/health` - Health check (returns "healthy")
- `/status` - Component statuses
- `/version` - Version "6.0.0", architecture
- `/metrics` - Prometheus metrics
- `/docs` - Swagger UI
- `/redoc` - ReDoc docs
- `/openapi.json` - OpenAPI spec

**Environment Variables**:
- `APP_NAME=ZQAutoNXG`, `HOST=0.0.0.0`, `PORT=8000`
- `CORS_ORIGINS=http://localhost:3000,http://localhost:8080` (comma-separated)
- `LOG_LEVEL=INFO` (not implemented), `GIT_COMMIT=unknown`

**Dependencies** (requirements.txt): FastAPI ≥0.115, Uvicorn[standard] ≥0.30, Pydantic ≥2.7, pydantic-settings ≥2.1, prometheus-client ≥0.20, NetworkX ≥3.3, httpx ≥0.27, cryptography ≥42.0

## Code Style

- Line length: 88 chars (Black) / 127 (Flake8)
- Python 3.11+ required
- **Copyright header** (REQUIRED in all new .py files):
```python
# Copyright © 2025 Zubin Qayam — ZQAutoNXG Powered by ZQ AI LOGIC
# Licensed under the Apache License, Version 2.0
```
- Trademarks: "ZQ AI LOGIC™" and "ZQAutoNXG" must be included in new files

## Validation

These instructions validated by: installing dependencies, running app/endpoints, linting with flake8 (0 errors), confirming pytest/pyproject.toml error, building Docker image, testing container health checks.

**Trust these instructions. Only search if**: instructions incomplete for your task, error not in Known Issues, or repo significantly updated since creation.
