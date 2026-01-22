# Copyright © 2025 Zubin Qayam — ZQAutoNXG Powered by ZQ AI LOGIC
# Licensed under the Apache License, Version 2.0

"""
Logs API router with WebSocket support.
"""

import asyncio
import json
import logging
from collections import deque
from datetime import datetime
from typing import Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

logger = logging.getLogger("zqautonxg.api.logs")
router = APIRouter(prefix="/logs", tags=["logs"])

# In-memory log storage (last 1000 entries)
# Use deque for O(1) appends and automatic size management
MAX_LOGS_HISTORY = 1000
logs_history: deque[dict[str, Any]] = deque(maxlen=MAX_LOGS_HISTORY)

# Active WebSocket connections
active_connections: list[WebSocket] = []


class LogEntry:
    """Log entry model."""

    def __init__(self, level: str, message: str, metadata: dict[str, Any] = None):
        self.timestamp = datetime.utcnow().isoformat()
        self.level = level
        self.message = message
        self.metadata = metadata or {}

    def to_dict(self) -> dict[str, Any]:
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
    # deque handles maxlen automatically, no need to manually pop
    logs_history.append(log_entry.to_dict())

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
        # Convert deque to list for slicing
        # We only send the last 100 logs to new connections
        history_snapshot = list(logs_history)
        for log in history_snapshot[-100:]:  # Send last 100 logs
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
async def get_logs_history(limit: int = 100) -> list[dict[str, Any]]:
    """Get historical logs."""
    # Convert deque to list to support slicing
    return list(logs_history)[-limit:]


@router.post("/query")
async def query_logs(
    level: str = None,
    search: str = None,
    limit: int = 100
) -> list[dict[str, Any]]:
    """Query logs with filters."""
    # Start with a reference to the deque
    filtered_logs = logs_history

    if level:
        # If filtering, we get a list
        filtered_logs = [log for log in filtered_logs if log["level"] == level.upper()]

    if search:
        # If filtering, we get a list
        filtered_logs = [
            log for log in filtered_logs
            if search.lower() in log["message"].lower()
        ]

    # If no filters were applied, filtered_logs is still a deque
    if isinstance(filtered_logs, deque):
        return list(filtered_logs)[-limit:]

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
