from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime,  Numeric
from sqlalchemy.orm import relationship
from .base import Base
# from user_server import user_server_table

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True, nullable=False)
    last_name = Column(String, index=True, default=None)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, index=True, default=None)
    password_hash = Column(String, nullable=False)
    password_server_hash = Column(String, default=None) # secret_code hash
    is_active = Column(Boolean, default=True)
    secret_code = Column(Integer, default=-1)
    account_id = Column(Integer, ForeignKey('accounts.id')) # New column
    expiration_date = Column(DateTime, default=None) # New column

    account = relationship("Account") # New relationship
    # Other fields and relationships as before...


# New Account model
class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    max_users = Column(Integer)
    duration_months = Column(Integer)
    cost_toman = Column(Numeric, nullable=False)

    users = relationship("User", back_populates="account") # New relationship

