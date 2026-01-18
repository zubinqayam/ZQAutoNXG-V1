
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from zqautonxg.app import app
from zqautonxg.api.v1.logs import logs_history, LogEntry, MAX_LOGS_HISTORY

@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c

@pytest.mark.asyncio
async def test_logs_history(client):
    # Clear history
    logs_history.clear()

    # Add some logs
    for i in range(5):
        logs_history.append(LogEntry("INFO", f"Message {i}").to_dict())

    response = await client.get("/api/v1/logs/history")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    assert data[0]["message"] == "Message 0"
    assert data[-1]["message"] == "Message 4"

@pytest.mark.asyncio
async def test_logs_query(client):
    logs_history.clear()
    logs_history.append(LogEntry("INFO", "Info message").to_dict())
    logs_history.append(LogEntry("ERROR", "Error message").to_dict())

    # Test level filter
    response = await client.post("/api/v1/logs/query", params={"level": "ERROR"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["level"] == "ERROR"

    # Test search
    response = await client.post("/api/v1/logs/query", params={"search": "Info"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["message"] == "Info message"

@pytest.mark.asyncio
async def test_deque_behavior(client):
    logs_history.clear()
    # Fill more than MAX
    for i in range(MAX_LOGS_HISTORY + 10):
        logs_history.append(LogEntry("INFO", f"Msg {i}").to_dict())

    assert len(logs_history) == MAX_LOGS_HISTORY
    # first message should be Msg 10 (since 0-9 popped)
    assert logs_history[0]["message"] == "Msg 10"

    response = await client.get("/api/v1/logs/history?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    assert data[-1]["message"] == f"Msg {MAX_LOGS_HISTORY + 9}"
