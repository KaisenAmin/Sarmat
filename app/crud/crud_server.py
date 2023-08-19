from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.server import Server as ServerModel
from schemas.server_schema import ServerCreate

def get_server(db: Session, server_id: int):
    return db.query(ServerModel).filter(ServerModel.id == server_id).first()


def get_servers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ServerModel).offset(skip).limit(limit).all()

def get_server_by_ip(db: Session, ip: int):
    return db.query(ServerModel).filter(ServerModel.ip == ip).first()

def create_server(db: Session, server: ServerCreate):
    db_server = ServerModel(**server.dict())
    db.add(db_server)
    db.commit()
    db.refresh(db_server)
    return db_server


def delete_server(db: Session, server_id: int):
    server = db.query(ServerModel).filter(ServerModel.id == server_id).first()

    if server is None:
        raise HTTPException(status_code=404, detail="Server not found.")
    
    db.delete(server)
    db.commit()

def delete_server_by_ip(db: Session, ip: str):
    server = db.query(ServerModel).filter(ServerModel.ip == ip).first()

    if server is None:
        raise HTTPException(status_code=404, detail="Server not found.")
    
    db.delete(server)
    db.commit()

def update_server(db: Session, server_id: int, server: ServerCreate):
    db_server = get_server(db, server_id)
    if db_server:
        for key, value in server.dict(exclude_unset=True).items():
            setattr(db_server, key, value)
        db.commit()
        db.refresh(db_server)
    return db_server
