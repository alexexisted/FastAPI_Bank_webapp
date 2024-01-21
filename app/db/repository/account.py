from sqlalchemy.orm import Session
from schemas.user import UserCreate, ShowUser
from db.models.user import User
from core.hashing import Hasher

"""
Here i made all functions which connected to account
and this functions are used in route_account.py
"""


def deposit(id: int, amount: int, db: Session):
    user = db.query(User).filter(User.id == id).first()
    try:
        if amount > 0:
            user.balance += amount
            db.commit()
            db.refresh(user)
            return user
    except Exception as e:
        print(e)
    return {"message": "Amount is less than zero"}


def withdraw(id: int, amount: int, db: Session):
    user = db.query(User).filter(User.id == id).first()
    try:
        if amount > 0 and user.balance >= amount:
            user.balance -= amount
            db.commit()
            db.refresh(user)
            return user
    except Exception as e:
        print(e)
    return {"message": "You don't have enough money on your account"}
