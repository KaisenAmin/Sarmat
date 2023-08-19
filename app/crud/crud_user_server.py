# crud_user_server.py
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from sqlalchemy.sql import select
from models.user import User as UserModel
from models.server import Server as ServerModel
from models.user_server import user_server_table
from fastapi import HTTPException


def create_user_server_association(db: Session, user_id: int, server_id: int, max_connections: int, active_connections: int, mac_address: str):
        # Fetch the user and server
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    server = db.query(ServerModel).filter(ServerModel.id == server_id).first()

    # Check if user and server exist
    if user is None or server is None:
        raise HTTPException(status_code=404, detail="User or server not found.")
    
    # Assuming that you have a many-to-many relationship with an association table user_server_table
    # You might have to adjust the following code according to the actual schema

    # Check if association already exists
    existing_association = db.execute(
        select(user_server_table)
        .where(user_server_table.c.user_id == user_id, user_server_table.c.server_id == server_id, user_server_table.c.mac_address == mac_address)
    ).first()

    if existing_association:
        # If association already exists, update it
        db.execute(
            user_server_table.update()
            .where(user_server_table.c.user_id == user_id, user_server_table.c.server_id == server_id)
            .values(
                max_connections=max_connections,
                active_connections=active_connections,  # Increment the active connections
                mac_address=mac_address
            )
        )
    else:
        # Create new association
        db.execute(
            user_server_table.insert().values(
                user_id=user_id,
                server_id=server_id,
                max_connections=max_connections,
                active_connections=active_connections,  # Increment the active connections
                mac_address=mac_address
            )
        )

    # Commit the changes
    db.commit()
# This function returns a list of servers that the given user can access.
def get_servers_by_user(db: Session, user_id: int):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return user.servers

# This function returns a list of users that can access a given server.
def get_users_by_server(db: Session, server_id: int):
    server = db.query(ServerModel).filter(ServerModel.id == server_id).first()
    if server is None:
        raise HTTPException(status_code=404, detail="Server not found.")
    return server.users

# This function allows a user to access a server by adding an entry to the user_server table.
# It also sets the maximum number of connections that the user can have to the server.
def add_user_to_server(db: Session, user_id: int, server_id: int, max_connections: int = 1):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    server = db.query(ServerModel).filter(ServerModel.id == server_id).first()
    if user is None or server is None:
        raise HTTPException(status_code=404, detail="User or server not found.")
    user.servers.append(server)
    # Here you should also update the 'max_connections' field in the user_server table.
    db.commit()

# This function removes a user's access to a server by deleting an entry from the user_server table.
def remove_user_from_server(db: Session, user_id: int, server_id: int):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    server = db.query(ServerModel).filter(ServerModel.id == server_id).first()
    if user is None or server is None:
        raise HTTPException(status_code=404, detail="User or server not found.")
    user.servers.remove(server)
    db.commit()

# This function updates the maximum number of connections that a user can have to a server.
def update_max_connections(db: Session, user_id: int, server_id: int, max_connections: int):
    # We need to find the user_server association object.
    user_server_association = db.execute(
        select(user_server_table)
        .where(user_server_table.c.user_id == user_id, user_server_table.c.server_id == server_id)
    ).first()
    if user_server_association is None:
        raise HTTPException(status_code=404, detail="No association found between the user and the server.")
    user_server_association.max_connections = max_connections
    db.commit()


def delete_user_server_association(db: Session, user_id: int, server_id: int, mac_address: str):
    association = user_server_table.delete().where(user_server_table.c.user_id == user_id).where(user_server_table.c.server_id == server_id).where(user_server_table.c.mac_address == mac_address)
    db.execute(association)
    db.commit()


def get_user_servers(db: Session, user_id: int):
    max_connections = db.query(func.max(user_server_table.c.active_connections)).scalar()
    
    associations = db.query(user_server_table).filter(
    and_(
        user_server_table.c.user_id == user_id,
        user_server_table.c.active_connections == max_connections
    )).all()
    
    # The 'associations' variable will now be a list, 
    # which could be empty if there are no matching records.
    
    return list(associations)