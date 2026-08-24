
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from zqautonxg.app import app, cors_origins


# Set the transport to ASGITransport for direct app testing
@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c

@pytest.mark.asyncio
async def test_root(client):
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["platform"] == "ZQAutoNXG"

@pytest.mark.asyncio
async def test_health(client):
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

@pytest.mark.asyncio
async def test_status(client):
    response = await client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["healthy", "degraded", "unhealthy"]
    assert data["components"]["telemetry_mesh"]["status"] == "ready"
    assert data["integrations"]["prometheus"]["status"] == "active"

@pytest.mark.asyncio
async def test_version(client):
    response = await client.get("/version")
    assert response.status_code == 200
    data = response.json()
    assert "build_date" in data


@pytest.mark.asyncio
async def test_ui(client):
    response = await client.get("/ui")
    assert response.status_code == 200
    assert "ZQAutoNXG" in response.text


def test_cors_origins_are_normalized():
    assert cors_origins
    assert all(origin == origin.strip() for origin in cors_origins)
    assert all(origin for origin in cors_origins)
