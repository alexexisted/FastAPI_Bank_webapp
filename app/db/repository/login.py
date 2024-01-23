from fastapi import Depends, HTTPException, status, Response, Request
from jose import jwt, JWTError
from core.config import settings

from sqlalchemy.orm import Session
from db.models.user import User
from core.hashing import Hasher
from db.session import get_db

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


def get_token(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return token


def get_current_user(token: str = Depends(get_token), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )

    try:
        # decode token to get the email from payload
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub") #get the email as username from token's payload
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(email=username, db=db) #get the user by email using get_user function
    if user is None:
        raise credentials_exception
    return user
