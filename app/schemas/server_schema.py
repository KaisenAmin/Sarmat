from pydantic import BaseModel 



class ServerBase(BaseModel):
    name: str 
    location: str
    ssh_port: int 
    user: str 
    password: str


class ServerCreate(ServerBase):
    ip: str
    port: int


class Server(ServerBase):
    id: int 
    is_running: bool 

    class Config:
        orm_mode = True 
        