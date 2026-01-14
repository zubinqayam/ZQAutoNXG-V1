
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from zqautonxg.app import app


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c

@pytest.mark.asyncio
async def test_get_network_topology(client):
    response = await client.get("/api/v1/network/topology")
    assert response.status_code == 200
    data = response.json()
    assert "nodes" in data
    assert "connections" in data
    assert "timestamp" in data
    assert len(data["nodes"]) == 4
    assert len(data["connections"]) == 3
    assert data["timestamp"] == "2025-01-10T08:00:00Z"
