# Copyright © 2025 Zubin Qayam — ZQAutoNXG Powered by ZQ AI LOGIC
# Licensed under the Apache License, Version 2.0

"""
Node configuration models for ZQAutoNXG platform.
"""

from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class NodeConfig(BaseModel):
    """Base node configuration."""
    id: UUID = Field(default_factory=uuid4)
    type: str  # scheduler, connector, search, etc.
    config: Dict[str, Any] = Field(default_factory=dict)
    enabled: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class SchedulerConfig(BaseModel):
    """Scheduler node configuration."""
    max_concurrent_jobs: int = Field(default=5, ge=1, le=100)
    retry_attempts: int = Field(default=3, ge=0, le=10)
    retry_delay_ms: int = Field(default=1000, ge=0)
    exponential_backoff: bool = True
    history_retention_days: int = Field(default=30, ge=1, le=365)
    priority_queue: bool = False


class ConnectorConfig(BaseModel):
    """Connector node configuration."""
    base_url: str
    auth_type: str = "none"  # bearer, basic, api_key, none
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    custom_headers: Dict[str, str] = Field(default_factory=dict)
    timeout_ms: int = Field(default=30000, ge=1000, le=300000)
    retry_on_failure: bool = True


class SearchNodeConfig(BaseModel):
    """Web search node configuration."""
    provider: str = "google"  # google, bing, duckduckgo, serpapi
    api_key: Optional[str] = None
    result_count: int = Field(default=10, ge=1, le=100)
    market: str = "en-US"
    proxy_rotation: bool = False
    user_agent: str = "desktop"  # desktop, mobile


class NodeStats(BaseModel):
    """Node statistics."""
    node_id: UUID
    total_executions: int = 0
    successful_executions: int = 0
    failed_executions: int = 0
    average_duration_ms: float = 0.0
    last_execution: Optional[datetime] = None


class RequestHistory(BaseModel):
    """HTTP request history record."""
    id: UUID = Field(default_factory=uuid4)
    node_id: UUID
    method: str
    endpoint: str
    status_code: int
    latency_ms: int
    request_body: Optional[Dict[str, Any]] = None
    response_body: Optional[Dict[str, Any]] = None
    request_headers: Dict[str, str] = Field(default_factory=dict)
    response_headers: Dict[str, str] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174002",
                "node_id": "123e4567-e89b-12d3-a456-426614174003",
                "method": "GET",
                "endpoint": "/api/data",
                "status_code": 200,
                "latency_ms": 125
            }
        }
    }
