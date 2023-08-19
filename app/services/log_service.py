from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas.log_schema import Log, LogCreate
from crud.crud_log import get_log, get_logs, create_log, delete_log, update_log
from .dependencies import get_db

router = APIRouter()

@router.get("/", response_model=List[Log])
def read_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logs = get_logs(db, skip=skip, limit=limit)
    return logs


@router.get("/{log_id}", response_model=Log)
def read_log(log_id: int, db: Session = Depends(get_db)):
    db_log = get_log(db, log_id=log_id)
    if db_log is None:
        raise HTTPException(status_code=404, detail="Log not found")
    return db_log


@router.post("/", response_model=Log)
def create_new_log(log: LogCreate, db: Session = Depends(get_db)):
    db_log = create_log(db=db, log=log)
    return db_log


@router.delete("/{log_id}", response_model=Log)
def delete_existing_log(log_id: int, db: Session = Depends(get_db)):
    delete_log(db=db, log_id=log_id)
    return {"detail": f"Log with id {log_id} deleted."}


@router.put("/{log_id}", response_model=Log)
def update_existing_log(log: LogCreate, log_id: int, db: Session = Depends(get_db)):
    db_log = update_log(db=db, log_id=log_id, log=log)
    return db_log
