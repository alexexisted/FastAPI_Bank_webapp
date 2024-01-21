from sqlalchemy.orm import Session
from db.models.user import User
from core.hashing import Hasher


"""
in route_login.py i will use get_user function,
decoding jwt token and comparing email from payload with email from user
"""
def get_user(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    return user


def authenticate_user(email: str, password: str, db: Session):
    user = get_user(email=email, db=db)
    print(user)
    if not user:
        return False
    if not Hasher.verify_password(password, user.password):
        return False
    return user