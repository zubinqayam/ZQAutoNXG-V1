from fastapi.testclient import TestClient
from zqautonxg.app import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["platform"] == "ZQAutoNXG"
    assert data["status"] == "operational"

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    # Prometheus format check (very basic)
    assert b"zqautonxg_requests_total" in response.content

def test_status():
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert "components" in data
    assert data["components"]["telemetry_mesh"] == "ready"

def test_version():
    response = client.get("/version")
    assert response.status_code == 200
    data = response.json()
    assert "version" in data
