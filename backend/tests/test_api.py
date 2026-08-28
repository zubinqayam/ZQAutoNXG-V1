from fastapi.testclient import TestClient

from zqautonxg.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["platform"] == "ZQAutoNXG"


def test_root() -> None:
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["platform"] == "ZQAutoNXG"
    assert data["status"] == "operational"


def test_flows_list() -> None:
    response = client.get("/flows/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
