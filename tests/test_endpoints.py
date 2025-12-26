from fastapi.testclient import TestClient
from zqautonxg.app import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "uptime" in data

def test_status():
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert "components" in data

def test_version():
    response = client.get("/version")
    assert response.status_code == 200
    data = response.json()
    assert "version" in data
