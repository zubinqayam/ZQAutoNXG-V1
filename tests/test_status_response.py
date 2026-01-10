# Copyright © 2025 Zubin Qayam — ZQAutoNXG Powered by ZQ AI LOGIC
# Licensed under the Apache License, Version 2.0

"""
Tests for enhanced status endpoint with detailed health checks.
"""

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
async def test_status_endpoint_structure(client):
    """Test the structure of the enhanced status endpoint."""
    response = await client.get("/status")
    assert response.status_code == 200
    data = response.json()
    
    # Check top-level fields
    assert "status" in data
    assert "platform" in data
    assert "version" in data
    assert "architecture" in data
    assert "brand" in data
    assert "license" in data
    assert "timestamp" in data
    assert "uptime_seconds" in data
    assert "components" in data
    assert "integrations" in data
    
    # Verify platform info
    assert data["platform"] == "ZQAutoNXG"
    assert data["version"] == "6.0.0"
    assert data["architecture"] == "G V2 NovaBase"
    assert data["brand"] == "Powered by ZQ AI LOGIC™"
    assert data["license"] == "Apache License 2.0"
    
    # Verify overall status is valid
    assert data["status"] in ["healthy", "degraded", "unhealthy"]
    
    # Verify uptime is a positive number
    assert isinstance(data["uptime_seconds"], (int, float))
    assert data["uptime_seconds"] >= 0


@pytest.mark.asyncio
async def test_status_components(client):
    """Test component health check details."""
    response = await client.get("/status")
    assert response.status_code == 200
    data = response.json()
    
    components = data["components"]
    
    # Verify all expected components are present
    expected_components = [
        "telemetry_mesh",
        "composer_agent",
        "vault_mesh",
        "policy_engine",
        "meta_learner",
        "rca_engine"
    ]
    
    for component in expected_components:
        assert component in components
        
        # Verify component structure
        component_data = components[component]
        assert "status" in component_data
        assert "message" in component_data
        assert "last_check" in component_data
        
        # Verify status is valid
        assert component_data["status"] in ["ready", "degraded", "unavailable", "unknown"]
        
        # Verify message is not empty
        assert isinstance(component_data["message"], str)
        assert len(component_data["message"]) > 0
        
        # Verify last_check is a valid timestamp
        assert isinstance(component_data["last_check"], str)


@pytest.mark.asyncio
async def test_status_integrations(client):
    """Test integration health check details."""
    response = await client.get("/status")
    assert response.status_code == 200
    data = response.json()
    
    integrations = data["integrations"]
    
    # Verify all expected integrations are present
    expected_integrations = [
        "zq_ai_logic",
        "prometheus",
        "docker"
    ]
    
    for integration in expected_integrations:
        assert integration in integrations
        
        # Verify integration structure
        integration_data = integrations[integration]
        assert "status" in integration_data
        assert "message" in integration_data
        assert "version" in integration_data
        
        # Verify status is valid
        assert integration_data["status"] in ["active", "configured", "inactive", "error"]
        
        # Verify message is not empty
        assert isinstance(integration_data["message"], str)
        assert len(integration_data["message"]) > 0
        
        # Verify version is present
        assert isinstance(integration_data["version"], str)


@pytest.mark.asyncio
async def test_status_prometheus_integration(client):
    """Test Prometheus integration specifically."""
    response = await client.get("/status")
    assert response.status_code == 200
    data = response.json()
    
    prometheus = data["integrations"]["prometheus"]
    assert prometheus["status"] == "active"
    assert "metrics" in prometheus["message"].lower() or "monitoring" in prometheus["message"].lower()


@pytest.mark.asyncio
async def test_health_endpoint_structure(client):
    """Test the health endpoint returns proper structure."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    
    # Check all required fields
    assert "status" in data
    assert "platform" in data
    assert "version" in data
    assert "architecture" in data
    assert "uptime" in data
    assert "timestamp" in data
    
    # Verify values
    assert data["status"] == "healthy"
    assert data["platform"] == "ZQAutoNXG"
    assert data["version"] == "6.0.0"
    assert data["uptime"] == "operational"
    assert isinstance(data["timestamp"], (int, float))


@pytest.mark.asyncio
async def test_status_response_is_consistent(client):
    """Test that multiple calls to status return consistent structure."""
    response1 = await client.get("/status")
    response2 = await client.get("/status")
    
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    data1 = response1.json()
    data2 = response2.json()
    
    # Keys should be the same
    assert set(data1.keys()) == set(data2.keys())
    
    # Component names should be the same
    assert set(data1["components"].keys()) == set(data2["components"].keys())
    
    # Integration names should be the same
    assert set(data1["integrations"].keys()) == set(data2["integrations"].keys())
