# Copyright © 2025 Zubin Qayam — ZQAutoNXG Powered by ZQ AI LOGIC
# Licensed under the Apache License, Version 2.0

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from zqautonxg.app import app


@pytest_asyncio.fixture
async def client():
    """Create test client."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


@pytest.mark.asyncio
async def test_create_workflow(client):
    """Test creating a new workflow."""
    workflow_data = {
        "name": "Test Workflow",
        "description": "A test workflow",
        "nodes": [],
        "edges": []
    }
    response = await client.post("/api/v1/workflows", json=workflow_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Workflow"
    assert data["status"] == "draft"
    assert "id" in data


@pytest.mark.asyncio
async def test_list_workflows(client):
    """Test listing workflows."""
    response = await client.get("/api/v1/workflows")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_workflow(client):
    """Test getting a specific workflow."""
    # First create a workflow
    workflow_data = {
        "name": "Test Workflow 2",
        "nodes": [],
        "edges": []
    }
    create_response = await client.post("/api/v1/workflows", json=workflow_data)
    workflow_id = create_response.json()["id"]
    
    # Now get it
    response = await client.get(f"/api/v1/workflows/{workflow_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == workflow_id
    assert data["name"] == "Test Workflow 2"


@pytest.mark.asyncio
async def test_update_workflow(client):
    """Test updating a workflow."""
    # Create workflow
    workflow_data = {
        "name": "Original Name",
        "nodes": [],
        "edges": []
    }
    create_response = await client.post("/api/v1/workflows", json=workflow_data)
    workflow_id = create_response.json()["id"]
    
    # Update it
    update_data = {"name": "Updated Name"}
    response = await client.put(f"/api/v1/workflows/{workflow_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"


@pytest.mark.asyncio
async def test_execute_workflow(client):
    """Test workflow execution."""
    # Create workflow
    workflow_data = {
        "name": "Executable Workflow",
        "nodes": [
            {
                "id": "node-1",
                "type": "scheduler",
                "position": {"x": 100, "y": 100},
                "data": {"label": "Test Node"}
            }
        ],
        "edges": []
    }
    create_response = await client.post("/api/v1/workflows", json=workflow_data)
    workflow_id = create_response.json()["id"]
    
    # Execute it
    response = await client.post(f"/api/v1/workflows/execute?workflow_id={workflow_id}")
    assert response.status_code == 202
    data = response.json()
    assert data["workflow_id"] == workflow_id
    assert data["status"] in ["running", "success"]


@pytest.mark.asyncio
async def test_get_node_status(client):
    """Test getting node statuses."""
    response = await client.get("/api/v1/nodes/status")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)


@pytest.mark.asyncio
async def test_get_logs_history(client):
    """Test getting log history."""
    response = await client.get("/api/v1/logs/history")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_network_topology(client):
    """Test getting network topology."""
    response = await client.get("/api/v1/network/topology")
    assert response.status_code == 200
    data = response.json()
    assert "nodes" in data
    assert "connections" in data
    assert isinstance(data["nodes"], list)
    assert isinstance(data["connections"], list)
