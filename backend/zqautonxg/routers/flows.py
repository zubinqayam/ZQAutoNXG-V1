from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/flows",
    tags=["flows"],
)

@router.post("/", response_model=schemas.Flow)
def create_flow(flow: schemas.FlowCreate, db: Session = Depends(get_db)):
    db_flow = models.Flow(**flow.model_dump())
    db.add(db_flow)
    db.commit()
    db.refresh(db_flow)
    return db_flow

@router.get("/", response_model=List[schemas.Flow])
def read_flows(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    flows = db.query(models.Flow).offset(skip).limit(limit).all()
    return flows

@router.get("/{flow_id}", response_model=schemas.Flow)
def read_flow(flow_id: int, db: Session = Depends(get_db)):
    db_flow = db.query(models.Flow).filter(models.Flow.id == flow_id).first()
    if db_flow is None:
        raise HTTPException(status_code=404, detail="Flow not found")
    return db_flow
