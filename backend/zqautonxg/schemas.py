from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class FlowBase(BaseModel):
    name: str
    description: Optional[str] = None
    definition: Dict[str, Any] = {}

class FlowCreate(FlowBase):
    pass

class Flow(FlowBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class RunBase(BaseModel):
    flow_id: int

class RunCreate(RunBase):
    pass

class Run(RunBase):
    id: int
    status: str
    logs: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    started_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ConnectionBase(BaseModel):
    name: str
    type: str
    config: Dict[str, Any]

class ConnectionCreate(ConnectionBase):
    pass

class Connection(ConnectionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
