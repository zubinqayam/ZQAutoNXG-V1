from pathlib import Path

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from zqautonxg.api.v1.logs import (
    MAX_LOGS_HISTORY,
    LogEntry,
    active_connections,
    broadcast_log,
    logs_history,
)
from zqautonxg.app import app


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as value:
        yield value


@pytest.fixture(autouse=True)
def reset_log_state():
    logs_history.clear()
    active_connections.clear()
    yield
    logs_history.clear()
    active_connections.clear()


@pytest.mark.asyncio
async def test_log_history_is_bounded():
    for index in range(MAX_LOGS_HISTORY + 5):
        await broadcast_log(LogEntry("info", f"message-{index}"))

    assert len(logs_history) == MAX_LOGS_HISTORY
    assert logs_history[0]["message"] == "message-5"
    assert logs_history[-1]["level"] == "INFO"


@pytest.mark.asyncio
async def test_failed_log_connection_is_removed():
    class FailedConnection:
        async def send_text(self, message):
            raise RuntimeError("connection closed")

    connection = FailedConnection()
    active_connections.append(connection)
    await broadcast_log(LogEntry("error", "failed send"))

    assert connection not in active_connections
    assert logs_history[-1]["message"] == "failed send"


@pytest.mark.asyncio
async def test_log_limit_is_validated(client):
    response = await client.get("/api/v1/logs/history?limit=0")
    assert response.status_code == 422

    response = await client.get(
        f"/api/v1/logs/history?limit={MAX_LOGS_HISTORY + 1}"
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_topology_has_current_timestamp_and_json_lists(client):
    response = await client.get("/api/v1/network/topology")
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data["nodes"], list)
    assert isinstance(data["connections"], list)
    assert data["timestamp"] != "2025-01-10T08:00:00Z"


def test_frontend_contains_vercel_observability_scripts():
    frontend = (
        Path(__file__).resolve().parents[1] / "frontend" / "index.html"
    ).read_text(encoding="utf-8")

    assert "/_vercel/insights/script.js" in frontend
    assert "/_vercel/speed-insights/script.js" in frontend
