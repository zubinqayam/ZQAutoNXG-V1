import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import importlib
import zqautonxg.app
from prometheus_client import REGISTRY

def test_cors_whitespace_handling():
    """
    Test that whitespace in CORS_ORIGINS is correctly handled.
    With the bug, ' http://localhost:8080' (with leading space) is treated as a valid origin,
    but 'http://localhost:8080' (sent by browser) does not match it due to the space.
    """
    # The origin we want to test
    origin = "http://localhost:8080"

    # We need to reload the app module because CORSMiddleware is configured at module level.
    # But reloading causes Prometheus client to complain about duplicate registration.
    # So we need to unregister the metrics if they exist.
    # Note: This is a bit hacky but necessary when reloading modules with global side effects.
    for name in list(REGISTRY._names_to_collectors.values()):
        try:
            REGISTRY.unregister(name)
        except KeyError:
            pass

    with patch.dict(os.environ, {"CORS_ORIGINS": "http://localhost:3000, http://localhost:8080"}):
        importlib.reload(zqautonxg.app)
        from zqautonxg.app import app

        client = TestClient(app)

        # Send request with Origin header
        response = client.get("/", headers={"Origin": origin})

        # Check if Access-Control-Allow-Origin header is present
        assert "access-control-allow-origin" in response.headers, \
            f"CORS header missing. Response headers: {response.headers}"
        assert response.headers["access-control-allow-origin"] == origin
