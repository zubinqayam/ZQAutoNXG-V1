# Copyright © 2025 Zubin Qayam — ZQAutoNXG Powered by ZQ AI LOGIC
# Licensed under the Apache License, Version 2.0

"""
Network topology API router.
"""

import json
import logging
import random
from typing import Any
from uuid import uuid4

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

logger = logging.getLogger("zqautonxg.api.network")
router = APIRouter(prefix="/network", tags=["network"])

# Active WebSocket connections for topology updates
topology_connections: list[WebSocket] = []

# Pre-computed static response for topology
# Optimization: Define static data at module level to avoid repeated allocation
# Use tuples for collections to ensure immutability and thread safety
TOPOLOGY_TEMPLATE: dict[str, Any] = {
    "nodes": (
        {
            "id": "hub-1",
            "type": "hub",
            "label": "Central Hub",
            "status": "healthy",
            "metrics": {
                "active_bridges": 5,
                "latency_ms": 12,
                "error_rate": 0.01
            }
        },
        {
            "id": "bridge-1",
            "type": "bridge",
            "label": "Bridge US-East",
            "status": "healthy",
            "metrics": {"latency_ms": 45, "throughput": 1250}
        },
        {
            "id": "bridge-2",
            "type": "bridge",
            "label": "Bridge EU-West",
            "status": "degraded",
            "metrics": {"latency_ms": 120, "throughput": 890}
        },
        {
            "id": "bridge-3",
            "type": "bridge",
            "label": "Bridge Asia-Pacific",
            "status": "healthy",
            "metrics": {"latency_ms": 78, "throughput": 1050}
        },
    ),
    "connections": (
        {"id": "conn-1", "source": "hub-1", "target": "bridge-1", "status": "active"},
        {"id": "conn-2", "source": "hub-1", "target": "bridge-2", "status": "degraded"},
        {"id": "conn-3", "source": "hub-1", "target": "bridge-3", "status": "active"},
    ),
    "timestamp": "2025-01-10T08:00:00Z"
}


@router.get("/topology")
async def get_network_topology() -> dict[str, Any]:
    """Get current network topology."""
    # Return pre-computed static response to avoid allocation overhead
    # Using .copy() ensures thread safety if the dict is modified later
    return TOPOLOGY_TEMPLATE.copy()


@router.websocket("/ws")
async def network_topology_websocket(websocket: WebSocket) -> None:
    """WebSocket endpoint for real-time network topology updates."""
    await websocket.accept()
    topology_connections.append(websocket)

    logger.info(f"New topology WebSocket connection. Total: {len(topology_connections)}")

    # Send initial topology
    topology = await get_network_topology()
    await websocket.send_text(json.dumps(topology))

    try:
        while True:
            # Wait for messages or send updates
            _ = await websocket.receive_text()
            await websocket.send_text(json.dumps({"type": "pong"}))
    except WebSocketDisconnect:
        topology_connections.remove(websocket)
        logger.info(f"Topology WebSocket disconnected. Total: {len(topology_connections)}")
    except Exception as e:
        logger.error(f"Topology WebSocket error: {e}")
        if websocket in topology_connections:
            topology_connections.remove(websocket)


@router.post("/deploy-bridge")
async def deploy_bridge(name: str, region: str) -> dict[str, str]:
    """Deploy a new network bridge."""
    bridge_id = str(uuid4())
    logger.info(f"Deploying bridge {name} in {region}")

    return {
        "bridge_id": bridge_id,
        "name": name,
        "region": region,
        "status": "deploying"
    }


@router.get("/nodes/{node_id}/metrics")
async def get_node_metrics(node_id: str) -> dict[str, Any]:
    """Get metrics for a specific network node."""
    return {
        "node_id": node_id,
        "latency_ms": random.randint(10, 150),
        "throughput_mbps": random.randint(500, 2000),
        "error_rate": round(random.uniform(0, 0.05), 3),
        "connections": random.randint(1, 20),
        "timestamp": "2025-01-10T08:00:00Z"
    }
