from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from schemas.user import UserCreate, ShowUser
from db.session import get_db
from db.repository.user import show_info
from db.repository.account import deposit, withdraw

router = APIRouter()
"""
here i made all routes which connected to account operations
"""

@router.post("/deposit", response_model=ShowUser)
async def deposit_money(id: int, amount: int, db: Session = Depends(get_db)):
    user = deposit(id=id, amount=amount, db=db)
    return user


@router.post("/withdraw", response_model=ShowUser)
async def withdraw_money(id: int, amount: int, db: Session = Depends(get_db)):
    user = withdraw(id=id, amount=amount, db=db)
    return user
