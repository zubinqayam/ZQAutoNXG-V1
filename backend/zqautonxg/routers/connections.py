from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/connections",
    tags=["connections"],
)

@router.post("/", response_model=schemas.Connection)
def create_connection(connection: schemas.ConnectionCreate, db: Session = Depends(get_db)):
    db_connection = models.Connection(**connection.model_dump())
    db.add(db_connection)
    db.commit()
    db.refresh(db_connection)
    return db_connection

@router.get("/", response_model=List[schemas.Connection])
def read_connections(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    connections = db.query(models.Connection).offset(skip).limit(limit).all()
    return connections

@router.get("/{connection_id}", response_model=schemas.Connection)
def read_connection(connection_id: int, db: Session = Depends(get_db)):
    db_connection = db.query(models.Connection).filter(models.Connection.id == connection_id).first()
    if db_connection is None:
        raise HTTPException(status_code=404, detail="Connection not found")
    return db_connection
