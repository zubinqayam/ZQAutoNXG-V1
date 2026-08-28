from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/runs",
    tags=["runs"],
)

@router.post("/", response_model=schemas.Run)
def create_run(run: schemas.RunCreate, db: Session = Depends(get_db)):
    # Verify flow exists
    db_flow = db.query(models.Flow).filter(models.Flow.id == run.flow_id).first()
    if not db_flow:
        raise HTTPException(status_code=404, detail="Flow not found")

    db_run = models.Run(**run.model_dump())
    db.add(db_run)
    db.commit()
    db.refresh(db_run)
    # In a real system, this would trigger the automation engine
    return db_run

@router.get("/", response_model=List[schemas.Run])
def read_runs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    runs = db.query(models.Run).offset(skip).limit(limit).all()
    return runs

@router.get("/{run_id}", response_model=schemas.Run)
def read_run(run_id: int, db: Session = Depends(get_db)):
    db_run = db.query(models.Run).filter(models.Run.id == run_id).first()
    if db_run is None:
        raise HTTPException(status_code=404, detail="Run not found")
    return db_run
