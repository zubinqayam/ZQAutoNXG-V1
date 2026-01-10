# Copyright © 2025 Zubin Qayam — ZQAutoNXG Powered by ZQ AI LOGIC
# Licensed under the Apache License, Version 2.0

"""
Status and health check models for ZQAutoNXG platform.
"""

from datetime import datetime
from enum import Enum
from typing import Dict, Optional

from pydantic import BaseModel, Field


class ComponentStatus(str, Enum):
    """Status of a system component."""
    READY = "ready"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"
    UNKNOWN = "unknown"


class IntegrationStatus(str, Enum):
    """Status of an integration."""
    ACTIVE = "active"
    CONFIGURED = "configured"
    INACTIVE = "inactive"
    ERROR = "error"


class OverallStatus(str, Enum):
    """Overall system status."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class ComponentCheck(BaseModel):
    """Health check result for a component."""
    status: ComponentStatus
    message: Optional[str] = None
    last_check: Optional[datetime] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "ready",
                "message": "Component is operational",
                "last_check": "2025-01-10T19:00:00Z"
            }
        }
    }


class IntegrationCheck(BaseModel):
    """Health check result for an integration."""
    status: IntegrationStatus
    message: Optional[str] = None
    version: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "active",
                "message": "Integration is connected",
                "version": "1.0.0"
            }
        }
    }


class StatusResponse(BaseModel):
    """Comprehensive status response for the platform."""
    status: OverallStatus
    platform: str
    version: str
    architecture: str
    brand: str
    license: str
    timestamp: datetime
    uptime_seconds: float = Field(..., description="Uptime in seconds")
    components: Dict[str, ComponentCheck]
    integrations: Dict[str, IntegrationCheck]

    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "healthy",
                "platform": "ZQAutoNXG",
                "version": "6.0.0",
                "architecture": "G V2 NovaBase",
                "brand": "Powered by ZQ AI LOGIC™",
                "license": "Apache License 2.0",
                "timestamp": "2025-01-10T19:00:00Z",
                "uptime_seconds": 3600.5,
                "components": {
                    "telemetry_mesh": {
                        "status": "ready",
                        "message": "Processing telemetry data",
                        "last_check": "2025-01-10T19:00:00Z"
                    }
                },
                "integrations": {
                    "prometheus": {
                        "status": "active",
                        "message": "Metrics collection active",
                        "version": "2.45.0"
                    }
                }
            }
        }
    }


class HealthResponse(BaseModel):
    """Simple health check response."""
    status: str
    platform: str
    version: str
    architecture: str
    uptime: str
    timestamp: float

    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "healthy",
                "platform": "ZQAutoNXG",
                "version": "6.0.0",
                "architecture": "G V2 NovaBase",
                "uptime": "operational",
                "timestamp": 1704916800.0
            }
        }
    }
