from sqlalchemy.orm import Session
from models.log import Log as LogModel
from schemas.log_schema import LogCreate


def get_log(db: Session, log_id: int):
    return db.query(LogModel).filter(LogModel.id == log_id).first()


def get_logs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(LogModel).offset(skip).limit(limit).all()


def create_log(db: Session, log: LogCreate):
    db_log = LogModel(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


def delete_log(db: Session, log_id: int):
    log = db.query(LogModel).filter(LogModel.id == log_id).first()
    db.delete(log)
    db.commit()


def update_log(db: Session, log_id: int, log: LogCreate):
    db_log = db.query(LogModel).filter(LogModel.id == log_id).first()
    for key, value in log.dict().items():
        setattr(db_log, key, value)
    db.commit()
    db.refresh(db_log)
    return db_log
