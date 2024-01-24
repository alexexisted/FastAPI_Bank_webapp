from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from db.models.user import User

from schemas.user import UserCreate, ShowUser
from db.session import get_db
from db.repository.user import create_new_user, show_info
from db.repository.login import get_current_user

router = APIRouter()

"""
There are all routers connected to operations with users
"""


@router.post("/register", response_model=ShowUser, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = create_new_user(user=user, db=db)
    return user


@router.get('/profile', response_model=ShowUser)
async def profile_info(request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user
