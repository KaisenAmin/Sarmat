# crud_account.py
from sqlalchemy.orm import Session
from models.user import Account as AccountModel
from models.user import User
from schemas.account_schema import AccountCreate
from models.user import User as UserModel
from datetime import datetime, timedelta
from fastapi import HTTPException

def get_account(db: Session, account_id: int):
    return db.query(AccountModel).filter(AccountModel.id == account_id).first()


def get_accounts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(AccountModel).offset(skip).limit(limit).all()


def create_new_account(db: Session, account: AccountCreate):
    # Check if the users exist
    users = []
    if len(account.user_ids) != 0:
        users = db.query(User).filter(User.id.in_(account.user_ids)).all()
    
        if not users:
            raise HTTPException(status_code=400, detail="Users not found")

    # Create the account
    db_account = AccountModel(
        name=account.name,
        max_users=account.max_users,
        duration_months=account.duration_months,
        cost_toman=account.cost_toman
    )
    
    db.add(db_account)
    db.commit()

    # Associate the users with the account
    for user in users:
        user.account_id = db_account.id
    db.commit()

    db.refresh(db_account)
    return db_account

def get_account_by_user_email_or_name(db: Session, email: str = None, first_name: str = None):
    query = db.query(AccountModel).join(UserModel, UserModel.account_id == AccountModel.id)

    if email:
        query = query.filter(UserModel.email == email)
    elif first_name:
        query = query.filter(UserModel.first_name == first_name)

    return query.first()


def update_user_expiration_date(account: AccountModel, duration_months: int, db: Session):
    # Get user by account_id
    user = db.query(UserModel).filter(UserModel.account_id == account.id).first()
    if user:
        # Update the expiration_date based on the new duration_months
        user.expiration_date = datetime.now() + timedelta(days=30 * duration_months)
        db.commit()