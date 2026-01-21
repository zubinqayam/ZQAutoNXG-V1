
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from zqautonxg.app import app
from zqautonxg.api.v1 import logs
from zqautonxg.api.v1.logs import LogEntry

# Set the transport to ASGITransport for direct app testing
@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c

@pytest.fixture(autouse=True)
def setup_logs():
    # Clear logs before each test
    logs.logs_history.clear()
    yield
    logs.logs_history.clear()

@pytest.mark.asyncio
async def test_get_history_empty(client):
    response = await client.get("/api/v1/logs/history")
    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.asyncio
async def test_get_history_populated(client):
    # Add some logs
    entry1 = LogEntry(level="INFO", message="Test log 1")
    entry2 = LogEntry(level="ERROR", message="Test log 2")
    await logs.broadcast_log(entry1)
    await logs.broadcast_log(entry2)

    response = await client.get("/api/v1/logs/history")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["message"] == "Test log 1"
    assert data[1]["message"] == "Test log 2"

@pytest.mark.asyncio
async def test_get_history_limit(client):
    # Add 5 logs
    for i in range(5):
        await logs.broadcast_log(LogEntry(level="INFO", message=f"Log {i}"))

    response = await client.get("/api/v1/logs/history?limit=3")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    # Should get last 3: Log 2, Log 3, Log 4
    assert data[0]["message"] == "Log 2"
    assert data[-1]["message"] == "Log 4"

@pytest.mark.asyncio
async def test_query_logs(client):
    await logs.broadcast_log(LogEntry(level="INFO", message="Info log"))
    await logs.broadcast_log(LogEntry(level="ERROR", message="Error log"))
    await logs.broadcast_log(LogEntry(level="INFO", message="Another Info log"))

    # Query by level
    response = await client.post("/api/v1/logs/query", params={"level": "INFO"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(d["level"] == "INFO" for d in data)

    # Query by search
    response = await client.post("/api/v1/logs/query", params={"search": "Error"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["message"] == "Error log"
