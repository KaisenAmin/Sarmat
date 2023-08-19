from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from .base import Base 
# from user_server import user_server_table

class Server(Base):
    __tablename__ = "servers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    location = Column(String, index=True)
    port = Column(Integer)
    ip = Column(String)
    ssh_port = Column(Integer)
    user = Column(String)
    password = Column(String)
    is_running = Column(Boolean, default=False)

    # users = relationship("User", secondary=user_server_table, back_populates="servers")
