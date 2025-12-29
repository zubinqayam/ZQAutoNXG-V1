
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from zqautonxg.app import app


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
    assert data["integrations"]["prometheus"] == "active"

@pytest.mark.asyncio
async def test_version(client):
    response = await client.get("/version")
    assert response.status_code == 200
    data = response.json()
    assert "build_date" in data

@pytest.mark.asyncio
async def test_metrics(client):
    response = await client.get("/metrics")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/plain; version=1.0.0; charset=utf-8"
    assert "zqautonxg_requests_total" in response.text
