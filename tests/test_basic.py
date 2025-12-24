from fastapi.testclient import TestClient

from zqautonxg.app import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["platform"] == "ZQAutoNXG"

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200

def test_status():
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json()["components"]["telemetry_mesh"] == "ready"

def test_version():
    response = client.get("/version")
    assert response.status_code == 200
    assert "version" in response.json()
