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
async def test_get_topology(client):
    response = await client.get("/api/v1/network/topology")
    assert response.status_code == 200
    data = response.json()
    assert "nodes" in data
    assert "connections" in data
    assert "timestamp" in data

    # Check strict structure
    assert isinstance(data["nodes"], list)
    assert len(data["nodes"]) == 4
    assert data["nodes"][0]["id"] == "hub-1"

    assert isinstance(data["connections"], list)
    assert len(data["connections"]) == 3
