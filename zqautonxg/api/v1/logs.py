# Copyright © 2025 Zubin Qayam — ZQAutoNXG Powered by ZQ AI LOGIC
# Licensed under the Apache License, Version 2.0

"""
Logs API router with WebSocket support.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Any, Dict, List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

logger = logging.getLogger("zqautonxg.api.logs")
router = APIRouter(prefix="/logs", tags=["logs"])

# In-memory log storage (last 1000 entries)
logs_history: List[Dict[str, Any]] = []
MAX_LOGS_HISTORY = 1000

# Active WebSocket connections
active_connections: List[WebSocket] = []


class LogEntry:
    """Log entry model."""
    
    def __init__(self, level: str, message: str, metadata: Dict[str, Any] = None):
        self.timestamp = datetime.utcnow().isoformat()
        self.level = level
        self.message = message
        self.metadata = metadata or {}
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "level": self.level,
            "message": self.message,
            "metadata": self.metadata,
        }


async def broadcast_log(log_entry: LogEntry) -> None:
    """Broadcast log entry to all connected WebSocket clients."""
    message = json.dumps(log_entry.to_dict())
    
    # Store in history
    logs_history.append(log_entry.to_dict())
    if len(logs_history) > MAX_LOGS_HISTORY:
        logs_history.pop(0)
    
    # Broadcast to all connections
    disconnected = []
    for connection in active_connections:
        try:
            await connection.send_text(message)
        except Exception as e:
            logger.error(f"Error broadcasting to connection: {e}")
            disconnected.append(connection)
    
    # Remove disconnected clients
    for connection in disconnected:
        active_connections.remove(connection)


@router.websocket("/ws")
async def logs_websocket(websocket: WebSocket) -> None:
    """WebSocket endpoint for real-time log streaming."""
    await websocket.accept()
    active_connections.append(websocket)
    
    logger.info(f"New WebSocket connection. Total connections: {len(active_connections)}")
    
    # Send recent history
    try:
        for log in logs_history[-100:]:  # Send last 100 logs
            await websocket.send_text(json.dumps(log))
    except Exception as e:
        logger.error(f"Error sending history: {e}")
    
    try:
        # Keep connection alive and handle incoming messages
        while True:
            data = await websocket.receive_text()
            # Echo back or handle commands
            await websocket.send_text(json.dumps({"type": "pong", "data": data}))
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        logger.info(f"WebSocket disconnected. Total connections: {len(active_connections)}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        if websocket in active_connections:
            active_connections.remove(websocket)


@router.get("/history")
async def get_logs_history(limit: int = 100) -> List[Dict[str, Any]]:
    """Get historical logs."""
    return logs_history[-limit:]


@router.post("/query")
async def query_logs(
    level: str = None,
    search: str = None,
    limit: int = 100
) -> List[Dict[str, Any]]:
    """Query logs with filters."""
    filtered_logs = logs_history
    
    if level:
        filtered_logs = [log for log in filtered_logs if log["level"] == level.upper()]
    
    if search:
        filtered_logs = [
            log for log in filtered_logs
            if search.lower() in log["message"].lower()
        ]
    
    return filtered_logs[-limit:]


# Background task to generate sample logs for demo
async def generate_sample_logs() -> None:
    """Generate sample logs for demonstration."""
    levels = ["DEBUG", "INFO", "WARN", "ERROR"]
    messages = [
        "Workflow execution started",
        "Node processing completed",
        "API request received",
        "Database connection established",
        "Cache miss for key",
    ]
    
    while True:
        await asyncio.sleep(5)  # Generate a log every 5 seconds
        
        if active_connections:
            import random
            level = random.choice(levels)
            message = random.choice(messages)
            
            log_entry = LogEntry(
                level=level,
                message=message,
                metadata={"node_id": f"node-{random.randint(1, 10)}"}
            )
            
            await broadcast_log(log_entry)
