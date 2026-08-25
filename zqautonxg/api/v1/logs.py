# Copyright © 2025 Zubin Qayam — ZQAutoNXG Powered by ZQ AI LOGIC
# Licensed under the Apache License, Version 2.0

"""Logs API router with bounded history and WebSocket support."""

import asyncio
import json
import logging
import random
from collections import deque
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect

logger = logging.getLogger("zqautonxg.api.logs")
router = APIRouter(prefix="/logs", tags=["logs"])

MAX_LOGS_HISTORY = 1000
logs_history: deque[dict[str, Any]] = deque(maxlen=MAX_LOGS_HISTORY)
active_connections: list[WebSocket] = []


class LogEntry:
    """Serializable application log entry."""

    def __init__(
        self,
        level: str,
        message: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.level = level.upper()
        self.message = message
        self.metadata = metadata or {}

    def to_dict(self) -> dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "level": self.level,
            "message": self.message,
            "metadata": self.metadata,
        }


async def _send_log(connection: WebSocket, message: str) -> Exception | None:
    try:
        await asyncio.wait_for(connection.send_text(message), timeout=5)
    except Exception as exc:
        return exc
    return None


async def broadcast_log(log_entry: LogEntry) -> None:
    """Store a log entry and broadcast it concurrently to connected clients."""
    log_dict = log_entry.to_dict()
    logs_history.append(log_dict)

    connections = list(active_connections)
    if not connections:
        return

    message = json.dumps(log_dict)
    results = await asyncio.gather(
        *(_send_log(connection, message) for connection in connections)
    )
    for connection, result in zip(connections, results):
        if result is not None:
            logger.warning("Removing failed log WebSocket: %s", result)
            if connection in active_connections:
                active_connections.remove(connection)


@router.websocket("/ws")
async def logs_websocket(websocket: WebSocket) -> None:
    """Stream recent and new application logs."""
    await websocket.accept()
    active_connections.append(websocket)
    logger.info(
        "New log WebSocket connection. Total connections: %s",
        len(active_connections),
    )

    try:
        for log_entry in list(logs_history)[-100:]:
            await websocket.send_text(json.dumps(log_entry))

        while True:
            data = await websocket.receive_text()
            await websocket.send_text(json.dumps({"type": "pong", "data": data}))
    except WebSocketDisconnect:
        pass
    except Exception:
        logger.exception("Log WebSocket failed")
    finally:
        if websocket in active_connections:
            active_connections.remove(websocket)
        logger.info(
            "Log WebSocket disconnected. Total connections: %s",
            len(active_connections),
        )


@router.get("/history")
async def get_logs_history(
    limit: int = Query(default=100, ge=1, le=MAX_LOGS_HISTORY),
) -> list[dict[str, Any]]:
    """Return the newest bounded log entries."""
    return list(logs_history)[-limit:]


@router.post("/query")
async def query_logs(
    level: str | None = None,
    search: str | None = None,
    limit: int = Query(default=100, ge=1, le=MAX_LOGS_HISTORY),
) -> list[dict[str, Any]]:
    """Query bounded log history with optional level and text filters."""
    filtered_logs = list(logs_history)

    if level:
        normalized_level = level.upper()
        filtered_logs = [
            log_entry
            for log_entry in filtered_logs
            if log_entry["level"] == normalized_level
        ]

    if search:
        normalized_search = search.casefold()
        filtered_logs = [
            log_entry
            for log_entry in filtered_logs
            if normalized_search in log_entry["message"].casefold()
        ]

    return filtered_logs[-limit:]


async def generate_sample_logs() -> None:
    """Generate demo logs only while at least one client is connected."""
    levels = ("DEBUG", "INFO", "WARN", "ERROR")
    messages = (
        "Workflow execution started",
        "Node processing completed",
        "API request received",
        "Database connection established",
        "Cache miss for key",
    )

    while True:
        await asyncio.sleep(5)
        if active_connections:
            await broadcast_log(
                LogEntry(
                    level=random.choice(levels),
                    message=random.choice(messages),
                    metadata={"node_id": f"node-{random.randint(1, 10)}"},
                )
            )
