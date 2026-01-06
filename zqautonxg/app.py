#!/usr/bin/env python3
# Copyright © 2025 Zubin Qayam — ZQAutoNXG Powered by ZQ AI LOGIC
# Licensed under the Apache License, Version 2.0

import logging
import os
import time
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest
from starlette.responses import Response

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

# Pre-computed response template for root endpoint
# Optimization: Define static response parts once to avoid recreation on every request
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

# Pre-initialized metric labels
# Optimization: Avoid label lookup overhead on every request
ROOT_REQUEST_METRIC = REQUEST_COUNT.labels(method="GET", endpoint="root")

@app.get("/")
async def root() -> dict:
    """Root endpoint with ZQAutoNXG information"""
    ROOT_REQUEST_METRIC.inc()
    logger.info("Root endpoint accessed")

    response = ROOT_RESPONSE_TEMPLATE.copy()
    response["timestamp"] = time.time()
    return response

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        log_level="info"
    )
