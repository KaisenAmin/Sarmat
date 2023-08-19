from pydantic import BaseModel, EmailStr 
from typing import Optional
import datetime


class UserBase(BaseModel):
    first_name: str 
    email: EmailStr


class UserCreate(UserBase):
    password_hash: str
    expiration_date: Optional[datetime.datetime]


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserInDB(UserBase):
    id: int
    is_active: bool 
    password_hash: str

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    is_active: bool
    expiration_date: Optional[datetime.datetime]

    class Config:
        orm_mode = True 

class ChangePasswordInput(BaseModel):
    email: str
    current_password: str
    new_password: str