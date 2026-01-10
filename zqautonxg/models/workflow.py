# Copyright © 2025 Zubin Qayam — ZQAutoNXG Powered by ZQ AI LOGIC
# Licensed under the Apache License, Version 2.0

"""
Workflow data models for ZQAutoNXG platform.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class WorkflowNode(BaseModel):
    """Individual node in a workflow."""
    id: str
    type: str  # scheduler, connector, search, etc.
    position: Dict[str, float]
    data: Dict[str, Any]


class WorkflowEdge(BaseModel):
    """Connection between workflow nodes."""
    id: str
    source: str
    target: str
    type: Optional[str] = "default"


class WorkflowCreate(BaseModel):
    """Model for creating a new workflow."""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    nodes: List[WorkflowNode] = Field(default_factory=list)
    edges: List[WorkflowEdge] = Field(default_factory=list)


class WorkflowUpdate(BaseModel):
    """Model for updating an existing workflow."""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    nodes: Optional[List[WorkflowNode]] = None
    edges: Optional[List[WorkflowEdge]] = None
    status: Optional[str] = None


class Workflow(BaseModel):
    """Complete workflow model."""
    id: UUID = Field(default_factory=uuid4)
    name: str
    description: Optional[str] = None
    status: str = "draft"  # draft, published, archived
    nodes: List[WorkflowNode] = Field(default_factory=list)
    edges: List[WorkflowEdge] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[UUID] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Data Processing Workflow",
                "description": "Automated data processing pipeline",
                "status": "published",
                "nodes": [
                    {
                        "id": "node-1",
                        "type": "scheduler",
                        "position": {"x": 100, "y": 100},
                        "data": {"label": "Schedule Job"}
                    }
                ],
                "edges": []
            }
        }
    }


class WorkflowExecution(BaseModel):
    """Workflow execution record."""
    id: UUID = Field(default_factory=uuid4)
    workflow_id: UUID
    status: str = "pending"  # pending, running, success, failed
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    duration_ms: Optional[int] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174001",
                "workflow_id": "123e4567-e89b-12d3-a456-426614174000",
                "status": "success",
                "duration_ms": 1250
            }
        }
    }
