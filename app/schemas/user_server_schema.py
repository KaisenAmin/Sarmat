from pydantic import BaseModel
from typing import List

class Server(BaseModel):
    id: int
    name: str
    ip_address: str
    # Add other fields as needed...

    class Config:
        orm_mode = True


class UserServerAssociation(BaseModel):
    user_id: int
    server_id: int
    active_connections: int
    max_connections: int

    class Config:
        orm_mode = True
