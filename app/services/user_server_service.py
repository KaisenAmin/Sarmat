from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .dependencies import get_db
from models.user import User
from models.server import Server 
from schemas.user_schema import User as UserSchema
from crud.crud_user_server import create_user_server_association, get_user_servers, delete_user_server_association
from schemas.user_server_schema import Server as ServerSchema
from pydantic import BaseModel
router = APIRouter()


class MaxUserReq(BaseModel):
    max_connections: int
    active_connections: int
    mac_address: str

class UserServer(BaseModel):
    user_id: int
    server_id: int
    max_connections: int
    active_connections: int
    mac_address: str

class UpdateActiveConnectionsRequest(BaseModel):
    active_connections: int

@router.post("/associate/{user_id}/{server_id}")
def associate_user_with_server(user_id: int, server_id: int, req: MaxUserReq, db: Session = Depends(get_db)):
    max_connections = req.max_connections
    active_connections = req.active_connections
    mac_address = req.mac_address

    create_user_server_association(db, user_id, server_id, max_connections, active_connections, mac_address)

    return {"message": "User and server have been associated and active connections incremented."}


@router.get("/user_servers/{user_id}") # Update this line
def get_servers_of_user(user_id: int, db: Session = Depends(get_db)):
    servers = get_user_servers(db, user_id)
    if servers is None:
        raise HTTPException(status_code=404, detail="User not found")
    return servers


# @router.get("/server_users/{server_id}", response_model=List[UserSchema])
# def get_users_of_server(server_id: int, db: Session = Depends(get_db)):
#     users = get_server_users(db, server_id)
#     if users is None:
#         raise HTTPException(status_code=404, detail="Server not found")
#     return users


@router.delete("/dissociate/{user_id}/{server_id}/{mac_address}")
def dissociate_user_from_server(user_id: int, server_id: int, mac_address: str, db: Session = Depends(get_db)):
    delete_user_server_association(db, user_id, server_id, mac_address)
    return {"message": "User and server have been dissociated."}


# @router.put("/update_active_connections/{user_id}")
# def update_active_connections_by_user_id(user_id: int, request: UpdateActiveConnectionsRequest, db: Session = Depends(get_db)):
#     active_connections = request.active_connections

#     result = update_active_connections(db, user_id, active_connections)

#     if result:
#         return {"message": "Active connections updated successfully."}
#     else:
#         raise HTTPException(status_code=400, detail="Error updating active connections.")
    
