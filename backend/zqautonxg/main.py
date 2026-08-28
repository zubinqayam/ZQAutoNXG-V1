#!/usr/bin/env python3
# Copyright © 2025 Zubin Qayam — ZQAutoNXG Powered by ZQ AI LOGIC
# Licensed under the Apache License, Version 2.0

import logging
import os
import time
from datetime import datetime, timezone
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest
from starlette.responses import Response

from .database import Base, engine
from .routers import connections, flows, runs

# ZQAutoNXG configuration
APP_NAME = os.getenv("APP_NAME", "ZQAutoNXG")
APP_VERSION = "6.0.0"
APP_BRAND = "Powered by ZQ AI LOGIC™"
APP_DESCRIPTION = "Next-Generation eXtended Automation Platform"
APP_START_TIME = time.time()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("zqautonxg")

# Create the persistence schema for the migrated backend.
Base.metadata.create_all(bind=engine)

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
        "url": "https://www.apache.org/licenses/LICENSE-2.0",
    },
)

cors_origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:3000,http://localhost:5173,"
        "http://localhost:8080,http://localhost:1420",
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Migrated product API.
app.include_router(flows.router)
app.include_router(runs.router)
app.include_router(connections.router)

REQUEST_COUNT = Counter(
    "zqautonxg_requests_total",
    "Total requests",
    ["method", "endpoint"],
)
HEALTH_CHECKS = Counter(
    "zqautonxg_health_checks_total",
    "Health check requests",
)
ROOT_REQUEST_METRIC = REQUEST_COUNT.labels(method="GET", endpoint="root")

ROOT_RESPONSE_TEMPLATE: dict[str, Any] = {
    "platform": APP_NAME,
    "version": APP_VERSION,
    "architecture": "G V2 NovaBase",
    "brand": APP_BRAND,
    "description": APP_DESCRIPTION,
    "status": "operational",
    "license": "Apache License 2.0",
    "copyright": "© 2025 Zubin Qayam — ZQAutoNXG",
}


@app.get("/")
async def root() -> dict[str, Any]:
    """Return basic platform information."""
    ROOT_REQUEST_METRIC.inc()
    response = ROOT_RESPONSE_TEMPLATE.copy()
    response["timestamp"] = time.time()
    return response


@app.get("/health")
async def health() -> dict[str, Any]:
    """Liveness/readiness endpoint used by CI and container health checks."""
    HEALTH_CHECKS.inc()
    return {
        "status": "healthy",
        "platform": APP_NAME,
        "version": APP_VERSION,
        "timestamp": time.time(),
    }


@app.get("/metrics")
async def metrics() -> Response:
    """Expose Prometheus metrics."""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/status")
async def status() -> dict[str, Any]:
    """Return a dependency-free operational status payload."""
    return {
        "status": "healthy",
        "platform": APP_NAME,
        "version": APP_VERSION,
        "architecture": "G V2 NovaBase",
        "brand": APP_BRAND,
        "license": "Apache License 2.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "uptime_seconds": time.time() - APP_START_TIME,
        "components": {
            "database": {
                "status": "ready",
                "message": "Persistence schema initialized",
            },
            "api": {
                "status": "ready",
                "message": "Flow, run, and connection routes registered",
            },
        },
        "integrations": {
            "prometheus": {
                "status": "active",
                "version": "latest",
            }
        },
    }


@app.get("/version")
async def version() -> dict[str, str]:
    """Return build/version information."""
    return {
        "platform": APP_NAME,
        "version": APP_VERSION,
        "architecture": "G V2 NovaBase",
        "brand": APP_BRAND,
        "license": "Apache License 2.0",
        "build_date": "2025-10-14",
        "git_commit": os.getenv("GIT_COMMIT", "unknown"),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        log_level="info",
    )
