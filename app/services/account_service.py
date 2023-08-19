# account_service.py
from typing import List
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from schemas.account_schema import Account as AccountSchema
from schemas.account_schema import AccountCreate
from schemas.account_schema import AccountUpdate
from .dependencies import get_db
from models.user import User, Account
from crud.curd_user import update_existing_user
from schemas.user_schema import UserCreate
from datetime import datetime, timedelta
from crud.crud_account import (
    get_account, 
    get_accounts, 
    create_new_account, 
    get_account_by_user_email_or_name,
    update_user_expiration_date
)

router = APIRouter()


@router.get("/", response_model=List[AccountSchema])
def read_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    accounts = get_accounts(db, skip=skip, limit=limit)
    return accounts


@router.get("/{account_id}", response_model=AccountSchema)
def read_account(account_id: int, db: Session = Depends(get_db)):
    db_account = get_account(db, account_id=account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account


@router.post("/", response_model=AccountSchema)
def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    return create_new_account(db=db, account=account)


@router.get("/by_user/email/{email}", response_model=AccountSchema)
def read_account_by_user_email(email: str, db: Session = Depends(get_db)):
    db_account = get_account_by_user_email_or_name(db, email=email)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account


@router.get("/by_user/first_name/{first_name}", response_model=AccountSchema)
def read_account_by_user_first_name(first_name: str, db: Session = Depends(get_db)):
    db_account = get_account_by_user_email_or_name(db, first_name=first_name)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account


@router.delete("/{account_id}", status_code=204)
def delete_account(account_id: int, db: Session = Depends(get_db)):
    # Fetch the account to be deleted
    db_account = db.query(Account).filter(Account.id == account_id).first()
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")

    # Delete the account
    db.delete(db_account)
    db.commit()


@router.post("/buy/{user_id}", response_model=AccountSchema)
def buy_account(account: AccountCreate, user_id: int, db: Session = Depends(get_db)):
    db_account = create_new_account(db=db, account=account)
    
    # Get user by user_id and update account_id and expiration_date
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.account_id = db_account.id
    user.expiration_date = datetime.now() + timedelta(days=30)
    
    db.commit()
    
    return db_account

@router.post("/buy_by_email/{user_email}", response_model=AccountSchema)
def buy_account_by_email(account: AccountCreate, user_email: str, db: Session = Depends(get_db)):
    db_account = create_new_account(db=db, account=account)
    
    # Get user by email and update account_id and expiration_date
    user = db.query(User).filter(User.email == user_email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.account_id = db_account.id
    user.expiration_date = datetime.now() + timedelta(days=30)
    
    db.commit()
    
    return db_account

@router.put("/{account_id}", response_model=AccountSchema)
def update_account(account_id: int, account_update: AccountUpdate, db: Session = Depends(get_db)):
    # Fetch the account to be updated
    db_account = db.query(Account).filter(Account.id == account_id).first()
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")

    # Update the fields
    for key, value in account_update.dict().items():
        if value is not None:
            setattr(db_account, key, value)

    # If duration_months is updated, update the user's expiration_date
    if account_update.duration_months is not None:
        update_user_expiration_date(db_account, account_update.duration_months, db)

    db.commit()

    return db_account


