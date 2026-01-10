#!/usr/bin/env python3
# Copyright © 2025 Zubin Qayam — ZQAutoNXG Powered by ZQ AI LOGIC
# Licensed under the Apache License, Version 2.0

import logging
import os
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.concurrency import run_in_threadpool
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest
from starlette.responses import Response
import sqlite3
from typing import Dict, Set, Any

# ZQAutoNXG Configuration
APP_NAME = os.getenv("APP_NAME", "ZQAutoNXG")
APP_VERSION = "6.0.0"
APP_BRAND = "Powered by ZQ AI LOGIC™"
APP_DESCRIPTION = "Next-Generation eXtended Automation Platform"

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("zqautonxg")

# Database Configuration
DB_PATH = "data/tickets.db"
os.makedirs("data", exist_ok=True)

def init_db() -> None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id TEXT PRIMARY KEY,
            subject TEXT,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

# Initialize DB on startup
# init_db() called in startup event to avoid module-level side effects

# WebSocket Connection Manager
class TicketConnectionManager:
    def __init__(self) -> None:
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, ticket_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        if ticket_id not in self.active_connections:
            self.active_connections[ticket_id] = set()
        self.active_connections[ticket_id].add(websocket)

    def disconnect(self, ticket_id: str, websocket: WebSocket) -> None:
        if ticket_id in self.active_connections:
            self.active_connections[ticket_id].discard(websocket)
            if not self.active_connections[ticket_id]:
                del self.active_connections[ticket_id]

    async def broadcast(self, ticket_id: str, message: Dict[str, Any]) -> None:
        if ticket_id in self.active_connections:
            dead_connections = set()
            for connection in self.active_connections[ticket_id]:
                try:
                    await connection.send_json(message)
                except Exception:
                    dead_connections.add(connection)

            for conn in dead_connections:
                self.disconnect(ticket_id, conn)

ws_manager = TicketConnectionManager()

# Create FastAPI application
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    on_startup=[init_db],
    description=f"{APP_DESCRIPTION} - {APP_BRAND}",
    contact={
        "name": "ZQ AI LOGIC™ Support",
        "email": "zubin.qayam@outlook.com",
    },
    license_info={
        "name": "Apache License 2.0",
        "url": "http://www.apache.org/licenses/LICENSE-2.0",
    }
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8080").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add GZip middleware for response compression
# Compressing responses > 1000 bytes significantly reduces network bandwidth usage
# and improves client response times, especially for the /metrics endpoint
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Prometheus metrics
REQUEST_COUNT = Counter('zqautonxg_requests_total', 'Total requests', ['method', 'endpoint'])
HEALTH_CHECKS = Counter('zqautonxg_health_checks_total', 'Health check requests')

# Performance: Pre-compute static response templates and metrics to avoid overhead in hot paths
ROOT_RESPONSE_TEMPLATE = {
    "platform": APP_NAME,
    "version": APP_VERSION,
    "architecture": "G V2 NovaBase",
    "brand": APP_BRAND,
    "description": APP_DESCRIPTION,
    "status": "operational",
    "license": "Apache License 2.0",
    "copyright": "© 2025 Zubin Qayam — ZQAutoNXG",
    "capabilities": [
        "AI-Powered Automation",
        "Extended Reality Integration",
        "Global-Scale Orchestration",
        "Next-Generation Algorithms",
        "Proprietary ZQ AI LOGIC™"
    ]
}

# Pre-initialize metrics labels to avoid lookup overhead
ROOT_REQUEST_METRIC = REQUEST_COUNT.labels(method="GET", endpoint="root")

@app.get("/")
async def root() -> dict:
    """Root endpoint with ZQAutoNXG information"""
    ROOT_REQUEST_METRIC.inc()
    # Performance: Logging in hot path is blocking and expensive
    # logger.info("Root endpoint accessed")

    # Use pre-computed template and merge dynamic timestamp
    # Dictionary unpacking is faster than .copy() + assignment for this case
    return {**ROOT_RESPONSE_TEMPLATE, "timestamp": time.time()}

@app.get("/health")
async def health() -> dict:
    """Health check endpoint"""
    HEALTH_CHECKS.inc()
    return {
        "status": "healthy",
        "platform": APP_NAME,
        "version": APP_VERSION,
        "architecture": "G V2 NovaBase",
        "timestamp": time.time(),
        "uptime": "operational"
    }

@app.get("/metrics")
async def metrics() -> Response:
    """
    Prometheus metrics endpoint.

    PERFORMANCE NOTE:
    Converted to `async def` to run directly on the event loop, avoiding the overhead
    of threadpool dispatch for this memory-bound operation. While generate_latest()
    is synchronous, it is typically fast enough to not block the loop significantly
    relative to the cost of context switching.
    """
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)

@app.get("/status")
async def status() -> dict:
    """Detailed status information"""
    return {
        "platform": APP_NAME,
        "version": APP_VERSION,
        "brand": APP_BRAND,
        "license": "Apache License 2.0",
        "components": {
            "telemetry_mesh": "ready",
            "composer_agent": "ready",
            "vault_mesh": "ready",
            "policy_engine": "ready",
            "meta_learner": "ready",
            "rca_engine": "ready"
        },
        "integrations": {
            "zq_ai_logic": "configured",
            "prometheus": "active",
            "docker": "containerized"
        }
    }

@app.get("/version")
async def version() -> dict:
    """Version information"""
    return {
        "platform": APP_NAME,
        "version": APP_VERSION,
        "architecture": "G V2 NovaBase",
        "brand": APP_BRAND,
        "license": "Apache License 2.0",
        "build_date": "2025-10-14",
        "git_commit": os.getenv("GIT_COMMIT", "unknown")
    }

def _check_ticket_exists(ticket_id: str) -> bool:
    """Synchronous DB check."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id FROM tickets WHERE id = ?", (ticket_id,))
    exists = cur.fetchone() is not None
    conn.close()
    return exists

@app.websocket("/ws/tickets/{ticket_id}")
async def websocket_ticket_endpoint(websocket: WebSocket, ticket_id: str) -> None:
    """
    WebSocket endpoint for real-time ticket updates.

    PERFORMANCE NOTE:
    Uses `run_in_threadpool` for the synchronous SQLite check to avoid blocking
    the asyncio event loop. Direct SQLite calls in `async def` would serialize
    requests and degrade performance.
    """
    # Performance: Offload blocking DB call to threadpool
    if not await run_in_threadpool(_check_ticket_exists, ticket_id):
        await websocket.close(code=1008, reason="Ticket not found")
        return

    await ws_manager.connect(ticket_id, websocket)
    try:
        while True:
            # Keep connection alive (client may send pings)
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(ticket_id, websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        log_level="info"
    )
