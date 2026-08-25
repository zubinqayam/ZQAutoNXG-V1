# Copyright © 2025 Zubin Qayam — ZQAutoNXG Powered by ZQ AI LOGIC
# Licensed under the Apache License, Version 2.0

"""Network topology API router."""

import json
import logging
import random
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

logger = logging.getLogger("zqautonxg.api.network")
router = APIRouter(prefix="/network", tags=["network"])

topology_connections: list[WebSocket] = []

_TOPOLOGY_NODES = (
    {
        "id": "hub-1",
        "type": "hub",
        "label": "Central Hub",
        "status": "healthy",
        "metrics": {
            "active_bridges": 5,
            "latency_ms": 12,
            "error_rate": 0.01,
        },
    },
    {
        "id": "bridge-1",
        "type": "bridge",
        "label": "Bridge US-East",
        "status": "healthy",
        "metrics": {"latency_ms": 45, "throughput": 1250},
    },
    {
        "id": "bridge-2",
        "type": "bridge",
        "label": "Bridge EU-West",
        "status": "degraded",
        "metrics": {"latency_ms": 120, "throughput": 890},
    },
    {
        "id": "bridge-3",
        "type": "bridge",
        "label": "Bridge Asia-Pacific",
        "status": "healthy",
        "metrics": {"latency_ms": 78, "throughput": 1050},
    },
)
_TOPOLOGY_CONNECTIONS = (
    {
        "id": "conn-1",
        "source": "hub-1",
        "target": "bridge-1",
        "status": "active",
    },
    {
        "id": "conn-2",
        "source": "hub-1",
        "target": "bridge-2",
        "status": "degraded",
    },
    {
        "id": "conn-3",
        "source": "hub-1",
        "target": "bridge-3",
        "status": "active",
    },
)


@router.get("/topology")
async def get_network_topology() -> dict[str, Any]:
    """Return the current sample topology without rebuilding static data."""
    return {
        "nodes": _TOPOLOGY_NODES,
        "connections": _TOPOLOGY_CONNECTIONS,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.websocket("/ws")
async def network_topology_websocket(websocket: WebSocket) -> None:
    """Stream topology messages."""
    await websocket.accept()
    topology_connections.append(websocket)
    logger.info(
        "New topology WebSocket connection. Total: %s",
        len(topology_connections),
    )

    try:
        await websocket.send_text(json.dumps(await get_network_topology()))
        while True:
            await websocket.receive_text()
            await websocket.send_text(json.dumps({"type": "pong"}))
    except WebSocketDisconnect:
        pass
    except Exception:
        logger.exception("Topology WebSocket failed")
    finally:
        if websocket in topology_connections:
            topology_connections.remove(websocket)
        logger.info(
            "Topology WebSocket disconnected. Total: %s",
            len(topology_connections),
        )


@router.post("/deploy-bridge")
async def deploy_bridge(name: str, region: str) -> dict[str, str]:
    """Return a deployment acknowledgement for a new network bridge."""
    bridge_id = str(uuid4())
    logger.info("Deploying bridge %s in %s", name, region)
    return {
        "bridge_id": bridge_id,
        "name": name,
        "region": region,
        "status": "deploying",
    }


@router.get("/nodes/{node_id}/metrics")
async def get_node_metrics(node_id: str) -> dict[str, Any]:
    """Return sample metrics for a network node."""
    return {
        "node_id": node_id,
        "latency_ms": random.randint(10, 150),
        "throughput_mbps": random.randint(500, 2000),
        "error_rate": round(random.uniform(0, 0.05), 3),
        "connections": random.randint(1, 20),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
