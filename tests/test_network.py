import pytest
from httpx import ASGITransport, AsyncClient

from zqautonxg.app import app

@pytest.mark.asyncio
async def test_get_network_topology():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/network/topology")
        assert response.status_code == 200
        data = response.json()

        # Verify structure
        assert "nodes" in data
        assert "connections" in data
        assert "timestamp" in data

        # Verify data types (JSON arrays)
        assert isinstance(data["nodes"], list)
        assert isinstance(data["connections"], list)

        # Verify content
        assert len(data["nodes"]) == 4
        assert len(data["connections"]) == 3

        # Check specific values to ensure data integrity
        hub = next(n for n in data["nodes"] if n["id"] == "hub-1")
        assert hub["type"] == "hub"
        assert hub["metrics"]["active_bridges"] == 5
