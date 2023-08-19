# account_schema.py
from pydantic import BaseModel
from typing import Optional, List


class AccountCreate(BaseModel):
    name: str
    max_users: int
    duration_months: int
    cost_toman: int
    user_ids: List[int]

class Account(BaseModel):
    id: int
    name: str
    max_users: int
    duration_months: int
    cost_toman: int

    class Config:
        orm_mode = True

class AccountUpdate(BaseModel):
    max_users: int = None
    duration_months: int = None
    name: str = None
    cost_toman: int = None