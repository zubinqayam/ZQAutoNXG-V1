# Copyright © 2025 Zubin Qayam — ZQAutoNXG Powered by ZQ AI LOGIC
# Licensed under the Apache License, Version 2.0

"""
Nodes API router.
"""

import logging
from typing import Any, Dict
from uuid import UUID

from fastapi import APIRouter, HTTPException

from zqautonxg.models.node import (
    ConnectorConfig,
    NodeConfig,
    NodeStats,
    SchedulerConfig,
    SearchNodeConfig,
)

logger = logging.getLogger("zqautonxg.api.nodes")
router = APIRouter(prefix="/nodes", tags=["nodes"])

# In-memory storage
nodes_db: Dict[UUID, NodeConfig] = {}
node_stats_db: Dict[UUID, NodeStats] = {}


@router.get("/status")
async def get_all_node_statuses() -> Dict[str, str]:
    """Get status of all nodes."""
    return {
        str(node_id): "enabled" if node.enabled else "disabled"
        for node_id, node in nodes_db.items()
    }


@router.post("/toggle/{node_id}")
async def toggle_node(node_id: UUID) -> Dict[str, bool]:
    """Enable or disable a node."""
    if node_id not in nodes_db:
        raise HTTPException(status_code=404, detail="Node not found")
    
    node = nodes_db[node_id]
    node.enabled = not node.enabled
    
    logger.info(f"Toggled node {node_id} to {'enabled' if node.enabled else 'disabled'}")
    return {"enabled": node.enabled}


@router.get("/{node_id}/config")
async def get_node_config(node_id: UUID) -> NodeConfig:
    """Get node configuration."""
    if node_id not in nodes_db:
        raise HTTPException(status_code=404, detail="Node not found")
    return nodes_db[node_id]


@router.put("/{node_id}/config")
async def update_node_config(node_id: UUID, config: Dict[str, Any]) -> NodeConfig:
    """Update node configuration."""
    if node_id not in nodes_db:
        # Create new node if it doesn't exist
        node = NodeConfig(id=node_id, type=config.get("type", "generic"), config=config)
        nodes_db[node_id] = node
    else:
        node = nodes_db[node_id]
        node.config = config
        from datetime import datetime
        node.updated_at = datetime.utcnow()
    
    logger.info(f"Updated config for node {node_id}")
    return node


@router.post("/{node_id}/test")
async def test_node(node_id: UUID) -> Dict[str, str]:
    """Test node configuration."""
    if node_id not in nodes_db:
        raise HTTPException(status_code=404, detail="Node not found")
    
    # Simulate test
    logger.info(f"Testing node {node_id}")
    return {"status": "success", "message": "Node configuration is valid"}


@router.get("/{node_id}/stats")
async def get_node_stats(node_id: UUID) -> NodeStats:
    """Get node statistics."""
    if node_id not in nodes_db:
        raise HTTPException(status_code=404, detail="Node not found")
    
    if node_id not in node_stats_db:
        node_stats_db[node_id] = NodeStats(node_id=node_id)
    
    return node_stats_db[node_id]
