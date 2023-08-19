from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from .base import Base
from .user import User
from .server import Server

user_server_table = Table('user_server', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('server_id', Integer, ForeignKey('servers.id')),
    Column('active_connections', Integer, default=0),
    Column('max_connections', Integer, default=1),
    Column('mac_address', String, default=None)
)

# Now, you can uncomment the relationship lines in User and Server models
User.servers = relationship("Server", secondary=user_server_table, back_populates="users")
Server.users = relationship("User", secondary=user_server_table, back_populates="servers")
