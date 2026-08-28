# Copyright © 2025 Zubin Qayam — ZQAutoNXG Powered by ZQ AI LOGIC
# Licensed under the Apache License, Version 2.0

"""
Workflows API router.
"""

import logging
from typing import Dict, List
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException

from zqautonxg.models.workflow import (
    Workflow,
    WorkflowCreate,
    WorkflowExecution,
    WorkflowUpdate,
)

logger = logging.getLogger("zqautonxg.api.workflows")
router = APIRouter(prefix="/workflows", tags=["workflows"])

# In-memory storage (replace with database in production)
workflows_db: Dict[UUID, Workflow] = {}
executions_db: Dict[UUID, List[WorkflowExecution]] = {}


@router.post("", response_model=Workflow, status_code=201)
async def create_workflow(workflow: WorkflowCreate) -> Workflow:
    """Create a new workflow."""
    new_workflow = Workflow(
        name=workflow.name,
        description=workflow.description,
        nodes=workflow.nodes,
        edges=workflow.edges,
    )
    workflows_db[new_workflow.id] = new_workflow
    logger.info(f"Created workflow {new_workflow.id}: {new_workflow.name}")
    return new_workflow


@router.get("/{workflow_id}", response_model=Workflow)
async def get_workflow(workflow_id: UUID) -> Workflow:
    """Get a workflow by ID."""
    if workflow_id not in workflows_db:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflows_db[workflow_id]


@router.get("", response_model=List[Workflow])
async def list_workflows() -> List[Workflow]:
    """List all workflows."""
    return list(workflows_db.values())


@router.put("/{workflow_id}", response_model=Workflow)
async def update_workflow(workflow_id: UUID, update: WorkflowUpdate) -> Workflow:
    """Update an existing workflow."""
    if workflow_id not in workflows_db:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    workflow = workflows_db[workflow_id]
    update_data = update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(workflow, field, value)
    
    from datetime import datetime
    workflow.updated_at = datetime.utcnow()
    
    logger.info(f"Updated workflow {workflow_id}")
    return workflow


@router.delete("/{workflow_id}", status_code=204)
async def delete_workflow(workflow_id: UUID) -> None:
    """Delete a workflow."""
    if workflow_id not in workflows_db:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    del workflows_db[workflow_id]
    if workflow_id in executions_db:
        del executions_db[workflow_id]
    
    logger.info(f"Deleted workflow {workflow_id}")


@router.post("/execute", response_model=WorkflowExecution, status_code=202)
async def execute_workflow(workflow_id: UUID) -> WorkflowExecution:
    """Execute a workflow in test mode."""
    if workflow_id not in workflows_db:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    execution = WorkflowExecution(workflow_id=workflow_id, status="running")
    
    if workflow_id not in executions_db:
        executions_db[workflow_id] = []
    executions_db[workflow_id].append(execution)
    
    logger.info(f"Started execution {execution.id} for workflow {workflow_id}")
    
    # Simulate execution (in production, this would be async)
    from datetime import datetime
    execution.status = "success"
    execution.completed_at = datetime.utcnow()
    execution.duration_ms = 1250
    execution.result = {"status": "completed", "nodes_executed": len(workflows_db[workflow_id].nodes)}
    
    return execution


@router.post("/activate")
async def activate_workflow(workflow_id: UUID) -> Dict[str, str]:
    """Activate a workflow for production."""
    if workflow_id not in workflows_db:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    workflow = workflows_db[workflow_id]
    workflow.status = "published"
    
    logger.info(f"Activated workflow {workflow_id}")
    return {"status": "activated", "workflow_id": str(workflow_id)}


@router.get("/{workflow_id}/history", response_model=List[WorkflowExecution])
async def get_workflow_history(workflow_id: UUID) -> List[WorkflowExecution]:
    """Get execution history for a workflow."""
    if workflow_id not in workflows_db:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    return executions_db.get(workflow_id, [])
