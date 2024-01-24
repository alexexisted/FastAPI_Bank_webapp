from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session

from db.models.user import User
from schemas.user import UserCreate, ShowUser
from db.session import get_db
from db.repository.user import show_info
from db.repository.account import deposit, withdraw
from db.repository.login import get_current_user

router = APIRouter()
"""
here i made all routes which connected to account operations
"""


@router.post("/withdraw", response_model=ShowUser)
async def withdraw_money(request: Request,
                         amount: int,
                         user: User = Depends(get_current_user),
                         db: Session = Depends(get_db)):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user = withdraw(id=user.id, amount=amount, db=db)
    return user


@router.post('/deposit', response_model=ShowUser)
async def deposit_money(request: Request,
                        amount: int,
                        user: User = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user = deposit(id=user.id, amount=amount, db=db)
    return user
