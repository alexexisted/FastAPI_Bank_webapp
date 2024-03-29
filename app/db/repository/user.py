from sqlalchemy.orm import Session
from schemas.user import UserCreate, ShowUser
from db.models.user import User
from core.hashing import Hasher

"""
Here locate all functions which connected to user and i use them in route_user.py

in create_new_user i'm collecting all data using UserCreate schema and add it to db
Also i'm using Hasher class to get the hash of password and add it to db
"""


def create_new_user(user: UserCreate, db: Session):
    user = User(
        name = user.name,
        surname = user.surname,
        email = user.email,
        password = Hasher.get_password_hash(user.password),
        is_superuser = False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def show_info(id: int, db: Session):
    user = db.query(User).filter(User.id == id).first()
    return user



