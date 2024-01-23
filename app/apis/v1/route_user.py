from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from db.models.user import User
from jose import JWTError

from schemas.user import UserCreate, ShowUser
from db.session import get_db
from db.repository.user import create_new_user, show_info
from apis.v1.route_login import get_current_user

router = APIRouter()

"""
There are all routers connected to operations with users
"""

@router.post("/create-user", response_model=ShowUser, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = create_new_user(user=user, db=db)
    return user


@router.get("/user/{id}", response_model=ShowUser)
async def show_user(id: int, db: Session = Depends(get_db)):
    user = show_info(id=id, db=db)
    return user

