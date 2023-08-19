from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LogBase(BaseModel):
    user_id: int
    server_id: int
    action: str

class LogCreate(LogBase):
    pass

class Log(LogBase):
    id: int
    timestamp: Optional[datetime] = None

    class Config:
        orm_mode = True
