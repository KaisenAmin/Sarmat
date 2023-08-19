from typing import List
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from schemas.user_schema import User, UserCreate, UserLogin, ChangePasswordInput
from sqlalchemy.exc import IntegrityError
from schemas.message import Message
from crud.curd_user import (
    reset_secret_code,
    delete_user_by_email,
    get_user_by_email,
    get_users,
    get_user,
    create_new_user,  # updated name
    delete_existing_user,  # updated name
    update_existing_user,  # updated name
    generate_password,
)

from .dependencies import get_db
from .auth_service import verify_password, get_password_hash
from fastapi import BackgroundTasks
import random
import yagmail
import re

router = APIRouter()

@router.get("/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/email/{user_email}", response_model=User)
def read_user_by_email(user_email: str, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user_email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/", response_model=Message)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
     # updated name
    try:
        db_user = create_new_user(db=db, user=user)
        if db_user:
            return {"detail": "account created successfully check your email"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e) + "amin")
        

@router.delete("/{user_id}", response_model=Message)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    deleted_user = delete_existing_user(db=db, user_id=user_id)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}


@router.delete("/email/{user_email}", response_model=Message)
def delete_user_by_email_endpoint(user_email: str, db: Session = Depends(get_db)):
    db_user = delete_user_by_email(db=db, email_id=user_email) 
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}


@router.put("/{user_id}", response_model=User)
def update_user(user: UserCreate, user_id: int, db: Session = Depends(get_db)):
    db_user = update_existing_user(db=db, user_id=user_id, user=user)  # updated name
    return db_user


@router.post("/check_email_verification/{user_email}")
async def check_email_verification(background_tasks: BackgroundTasks, user_email: str, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user_email)
    if db_user is None:
        return {"detail": "User not found"}

    # Generate a random 4-digit code
    secret_code = random.randint(1000, 9999)

    # Save the secret code to the user's record
    db_user.secret_code = secret_code
    db.commit()

    # Send the secret code via email
    yag = yagmail.SMTP("amintahmasebi479@gmail.com", "dciegtrmmdsmfdvz")
    yag.send(
        to=user_email,
        subject="Your verification code",
        contents=f"Your verification code is {secret_code}",
    )

    background_tasks.add_task(reset_secret_code, user_email, db)

    return {"detail": "Verification code sent to email!", "secret_code": secret_code}


@router.post("/login_authentication", response_model=Message)
async def login_authentication(user: UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not verify_password(user.password, db_user.password_hash):
       raise HTTPException(status_code=400, detail="Incorrect password")

    raise HTTPException(status_code=200, detail="Login successful")


@router.post("/change_password", response_model=Message)
async def change_password(change_password_input: ChangePasswordInput, db: Session = Depends(get_db)):
    email = change_password_input.email
    current_password = change_password_input.current_password
    new_password = change_password_input.new_password
    
    # Validate new password
    pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[_&])[A-Za-z\d_&]+$')
    if not pattern.match(new_password):
        return HTTPException(status_code=400, detail="New password must contain a combination of uppercase and lowercase letters, numbers, dashes, and ampersands.")

    # Check if user exists
    db_user = get_user_by_email(db, email)
    if db_user is None:
        return HTTPException(status_code=404, detail="User not found")

    # Check if the current password is correct
    if not verify_password(current_password, db_user.password_hash):
        return HTTPException(status_code=400, detail="Incorrect current password")
    
    # Update the password
    db_user.password_hash = get_password_hash(new_password) # This should ideally be hashed before saving
    db.commit()

    return {"detail": "Password successfully updated"}


@router.get("/get_password_hash/{user_email}", response_model=str)
def get_password_hash_for_user(user_email: str, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user_email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user.password_hash


@router.post("/generate_and_send_password/{user_email}", response_model=Message)
async def generate_and_send_password(user_email: str, db: Session = Depends(get_db)):
    # Fetch the user by email
    db_user = get_user_by_email(db, user_email)
    
    # If the user does not exist, raise an exception
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Generate a new password
    new_password = generate_password()

    # Hash the new password and save it
    db_user.password_hash = get_password_hash(new_password)
    db.commit()

    # Send the new password via email
    yag = yagmail.SMTP("amintahmasebi479@gmail.com", "dciegtrmmdsmfdvz")
    yag.send(
        to=user_email,
        subject="Your new password",
        contents=f"Your new password is {new_password}",
    )

    return {"detail": "New password sent to email!"}