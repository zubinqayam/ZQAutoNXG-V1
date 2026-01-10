#!/usr/bin/env python3
# Copyright © 2025 Zubin Qayam — ZQAutoNXG Powered by ZQ AI LOGIC
# Licensed under the Apache License, Version 2.0

import asyncio
import logging
import os
import time
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest
from starlette.responses import Response

from contextlib import asynccontextmanager

# Import API routers
from zqautonxg.api.v1 import logs, network, nodes, workflows

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


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    asyncio.create_task(logs.generate_sample_logs())
    logger.info("ZQAutoNXG platform started successfully")
    yield
    # Shutdown
    logger.info("ZQAutoNXG platform shutting down")


# Create FastAPI application
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description=f"{APP_DESCRIPTION} - {APP_BRAND}",
    contact={
        "name": "ZQ AI LOGIC™ Support",
        "email": "zubin.qayam@outlook.com",
    },
    license_info={
        "name": "Apache License 2.0",
        "url": "http://www.apache.org/licenses/LICENSE-2.0",
    },
    lifespan=lifespan,
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

# Include API routers
app.include_router(workflows.router, prefix="/api/v1")
app.include_router(nodes.router, prefix="/api/v1")
app.include_router(logs.router, prefix="/api/v1")
app.include_router(network.router, prefix="/api/v1")

# Serve frontend static files if available
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_path):
    # Serve index.html at /ui
    @app.get("/ui")
    async def serve_ui():
        """Serve the web interface."""
        index_path = os.path.join(frontend_path, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        return {"message": "Frontend not available"}
    
    logger.info(f"Frontend available at /ui")


# Prometheus metrics
REQUEST_COUNT = Counter('zqautonxg_requests_total', 'Total requests', ['method', 'endpoint'])
HEALTH_CHECKS = Counter('zqautonxg_health_checks_total', 'Health check requests')

# Pre-initialize metric labels to avoid map lookup overhead on every request
ROOT_REQUEST_METRIC = REQUEST_COUNT.labels(method="GET", endpoint="root")

# Pre-compute static response parts to avoid allocation on every request
ROOT_RESPONSE_TEMPLATE: dict[str, Any] = {
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

HEALTH_RESPONSE_TEMPLATE: dict[str, Any] = {
    "status": "healthy",
    "platform": APP_NAME,
    "version": APP_VERSION,
    "architecture": "G V2 NovaBase",
    "uptime": "operational"
}

STATUS_RESPONSE_TEMPLATE: dict[str, Any] = {
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

VERSION_RESPONSE_TEMPLATE: dict[str, Any] = {
    "platform": APP_NAME,
    "version": APP_VERSION,
    "architecture": "G V2 NovaBase",
    "brand": APP_BRAND,
    "license": "Apache License 2.0",
    "build_date": "2025-10-14",
    "git_commit": os.getenv("GIT_COMMIT", "unknown")
}

@app.get("/")
async def root():
    """Root endpoint with ZQAutoNXG information"""
    ROOT_REQUEST_METRIC.inc()
    logger.info("Root endpoint accessed")

    response = ROOT_RESPONSE_TEMPLATE.copy()
    response["timestamp"] = time.time()
    return response

@app.get("/health")
async def health():
    """Health check endpoint"""
    HEALTH_CHECKS.inc()

    response = HEALTH_RESPONSE_TEMPLATE.copy()
    response["timestamp"] = time.time()
    return response

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)

@app.get("/status")
async def status():
    """Detailed status information"""
    # Use pre-computed template to avoid dictionary allocation overhead
    return STATUS_RESPONSE_TEMPLATE.copy()

@app.get("/version")
async def version():
    """Version information"""
    # Use pre-computed template to avoid dictionary allocation overhead
    return VERSION_RESPONSE_TEMPLATE.copy()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        log_level="info"
    )
