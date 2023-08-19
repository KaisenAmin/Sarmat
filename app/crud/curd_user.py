# crud_user.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from models.user import User as UserModel
from schemas.user_schema import UserCreate
from services.auth_service import get_password_hash
import secrets
import string 
import asyncio


def generate_password(size: int = 8):
    # Ensure the size is at least 8
    size = max(size, 8)
    alphabet = string.ascii_letters + string.digits + '_&'

    while True:
        password = ''.join(secrets.choice(alphabet) for _ in range(size))
        if (any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and any(c.isdigit() for c in password)
            and any(c in ['_','&'] for c in password)):
            return password
        
def create_secret_password(length: int) -> str:
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for i in range(length))
    return password

def get_user(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserModel).offset(skip).limit(limit).all()

def get_user_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()

def create_new_user(db: Session, user: UserCreate):
    try:
        existing_user = db.query(UserModel).filter(UserModel.email == user.email).first()
        if existing_user is not None:
            raise {'detail': 'User already registered'}

        hashed_password = get_password_hash(user.password_hash)
        secret_pass = create_secret_password(10)
        print(secret_pass)
        value = get_password_hash(secret_pass)

        db_user = UserModel(
            first_name=user.first_name,
            email=user.email,
            password_hash=hashed_password,
            password_server_hash=value,
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    except:
        db.rollback()
        raise {'detail': "An error occurred while creating the user."}


def delete_existing_user(db: Session, user_id: int):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()  # Assuming User is your model class
    if user is None:
        return None
    db.delete(user)
    db.commit()
    return user


def delete_user_by_email(db: Session, email_id: str):
    user = db.query(UserModel).filter(UserModel.email == email_id).first()
    if user is None:
        return None
    db.delete(user)
    db.commit()

    return user
 
def update_existing_user(db: Session, user_id: int, user: UserCreate, account_id: int = None):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    
    if db_user:
        db_user.email = user.email
        db_user.first_name = user.first_name
        db_user.last_name = user.last_name
        db_user.phone = user.phone
        db_user.password_hash = get_password_hash(user.password)  # changed here
        
        # Check if account_id is provided and update it
        if account_id:
            db_user.account_id = account_id
        
        db.commit()
        db.refresh(db_user)
    else:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user


async def reset_secret_code(user_email: str, db: Session):
    # Wait for 1 minute
    await asyncio.sleep(60)

    # Get the user from the database
    db_user = get_user_by_email(db, user_email)
    if db_user:
        # Reset the secret code
        db_user.secret_code = -1
        db.commit()
