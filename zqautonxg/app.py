#!/usr/bin/env python3
# Copyright © 2025 Zubin Qayam — ZQAutoNXG Powered by ZQ AI LOGIC
# Licensed under the Apache License, Version 2.0

import asyncio
import logging
import os
import time
from contextlib import asynccontextmanager, suppress
from datetime import datetime, timezone
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest
from starlette.responses import FileResponse, Response


# Import API routers
from zqautonxg.api.v1 import logs, network, nodes, workflows

# Import models
from zqautonxg.models.status import (
    ComponentCheck,
    ComponentStatus,
    HealthResponse,
    IntegrationCheck,
    IntegrationStatus,
    OverallStatus,
    StatusResponse,
)

# ZQAutoNXG Configuration
APP_NAME = os.getenv("APP_NAME", "ZQAutoNXG")
APP_VERSION = "6.0.0"
APP_BRAND = "Powered by ZQ AI LOGIC™"
APP_DESCRIPTION = "Next-Generation eXtended Automation Platform"
GIT_COMMIT = (
    os.getenv("GIT_COMMIT")
    or os.getenv("VERCEL_GIT_COMMIT_SHA")
    or os.getenv("GITHUB_SHA")
    or "unknown"
)

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("zqautonxg")

# Application start time for uptime calculation
APP_START_TIME = time.time()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Start and stop application-owned background tasks."""
    sample_log_task = asyncio.create_task(logs.generate_sample_logs())
    logger.info("ZQAutoNXG platform started successfully")
    try:
        yield
    finally:
        sample_log_task.cancel()
        with suppress(asyncio.CancelledError):
            await sample_log_task
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
cors_origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS", "http://localhost:3000,http://localhost:8080"
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

@app.get("/")
async def root():
    """Root endpoint with ZQAutoNXG information"""
    ROOT_REQUEST_METRIC.inc()
    logger.info("Root endpoint accessed")

    response = ROOT_RESPONSE_TEMPLATE.copy()
    response["timestamp"] = time.time()
    return response

@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Liveness check for the running API process."""
    HEALTH_CHECKS.inc()
    return HealthResponse(
        status="healthy",
        platform=APP_NAME,
        version=APP_VERSION,
        architecture="G V2 NovaBase",
        uptime_seconds=time.time() - APP_START_TIME,
        timestamp=time.time(),
    )


@app.get("/readyz")
async def readiness() -> dict[str, Any]:
    """Readiness check used by container and Kubernetes orchestrators."""
    return {
        "status": "ready",
        "platform": APP_NAME,
        "version": APP_VERSION,
        "architecture": "G V2 NovaBase",
        "git_commit": GIT_COMMIT,
    }


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)

@app.get("/status", response_model=StatusResponse)
async def status() -> StatusResponse:
    """Detailed status information with comprehensive health checks"""
    now = datetime.now(timezone.utc)
    uptime = time.time() - APP_START_TIME
    
    # Report unprobed capability modules honestly. Operators can mark them
    # ready only after wiring real probes through ZQ_COMPONENTS_READY.
    component_state = (
        ComponentStatus.READY
        if os.getenv("ZQ_COMPONENTS_READY", "").lower() in {"1", "true", "yes"}
        else ComponentStatus.UNKNOWN
    )
    component_message = (
        "Readiness asserted by ZQ_COMPONENTS_READY"
        if component_state == ComponentStatus.READY
        else "No runtime readiness probe is configured"
    )
    components = {
        name: ComponentCheck(
            status=component_state,
            message=component_message,
            last_check=now,
        )
        for name in (
            "telemetry_mesh",
            "composer_agent",
            "vault_mesh",
            "policy_engine",
            "meta_learner",
            "rca_engine",
        )
    }

    zq_enabled = os.getenv("ZQ_AI_LOGIC_ENABLED", "").lower() in {
        "1",
        "true",
        "yes",
    }
    container_runtime = os.getenv("CONTAINER_RUNTIME")
    integrations = {
        "zq_ai_logic": IntegrationCheck(
            status=(
                IntegrationStatus.CONFIGURED
                if zq_enabled
                else IntegrationStatus.INACTIVE
            ),
            message=(
                "ZQ AI LOGIC integration enabled"
                if zq_enabled
                else "ZQ AI LOGIC integration is not enabled"
            ),
            version=os.getenv("ZQ_AI_LOGIC_VERSION", "unknown"),
        ),
        "prometheus": IntegrationCheck(
            status=IntegrationStatus.ACTIVE,
            message="Prometheus metrics endpoint is active",
            version=os.getenv("PROMETHEUS_CLIENT_VERSION", "bundled"),
        ),
        "container_runtime": IntegrationCheck(
            status=(
                IntegrationStatus.CONFIGURED
                if container_runtime
                else IntegrationStatus.INACTIVE
            ),
            message=(
                f"Container runtime: {container_runtime}"
                if container_runtime
                else "No container runtime was declared"
            ),
            version=container_runtime or "unknown",
        ),
    }

    # Determine overall status based on components (single pass)
    overall_status = OverallStatus.HEALTHY
    degraded_components = []
    unavailable_components = []
    
    for name, check in components.items():
        if check.status == ComponentStatus.UNAVAILABLE:
            unavailable_components.append(name)
        elif check.status == ComponentStatus.DEGRADED:
            degraded_components.append(name)
    
    if unavailable_components:
        overall_status = OverallStatus.UNHEALTHY
    elif degraded_components:
        overall_status = OverallStatus.DEGRADED
    
    return StatusResponse(
        status=overall_status,
        platform=APP_NAME,
        version=APP_VERSION,
        architecture="G V2 NovaBase",
        brand=APP_BRAND,
        license="Apache License 2.0",
        timestamp=now,
        uptime_seconds=uptime,
        components=components,
        integrations=integrations
    )

@app.get("/version")
async def version():
    """Version information"""
    return {
        "platform": APP_NAME,
        "version": APP_VERSION,
        "architecture": "G V2 NovaBase",
        "brand": APP_BRAND,
        "license": "Apache License 2.0",
        "build_date": os.getenv("BUILD_DATE", "unknown"),
        "git_commit": GIT_COMMIT
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        log_level="info"
    )
