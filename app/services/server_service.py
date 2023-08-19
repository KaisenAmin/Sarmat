from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas.server_schema import Server, ServerCreate
from crud.crud_server import (
    get_server, get_servers, create_server, delete_server, update_server, get_server_by_ip, delete_server_by_ip)
from .dependencies import get_db

router = APIRouter()

@router.get("/", response_model=List[Server])
def read_servers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    servers = get_servers(db, skip=skip, limit=limit)
    return servers


@router.get("/ip/{ip}", response_model=Server)
def read_server_by_ip(ip: str, db: Session = Depends(get_db)):
    servers = get_server_by_ip(db, ip)
    return servers

@router.get("/{server_id}", response_model=Server)
def read_server(server_id: int, db: Session = Depends(get_db)):
    db_server = get_server(db, server_id=server_id)
    if db_server is None:
        raise HTTPException(status_code=404, detail="Server not found")
    return db_server


@router.post("/", response_model=Server)
def create_new_server(server: ServerCreate, db: Session = Depends(get_db)):
    db_server = create_server(db=db, server=server)
    return db_server


@router.delete("/{server_id}", status_code=200)
def delete_existing_server(server_id: int, db: Session = Depends(get_db)):
    delete_server(db=db, server_id=server_id)
    return {"detail": f"Server with id {server_id} deleted."}


@router.delete("/ip/{ip}", status_code=200)
def delete_existing_server_by_ip(ip: str, db: Session = Depends(get_db)):
    delete_server_by_ip(db=db, ip=ip)
    return {"detail": f"Server with ip {ip} deleted."}


@router.put("/{server_id}", response_model=Server)
def update_existing_server(server: ServerCreate, server_id: int, db: Session = Depends(get_db)):
    db_server = update_server(db=db, server_id=server_id, server=server)
    return db_server
