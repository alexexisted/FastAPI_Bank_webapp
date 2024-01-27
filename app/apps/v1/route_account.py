from fastapi import APIRouter, Depends, Request, HTTPException, Response
from fastapi.templating import Jinja2Templates
from fastapi import responses, status, Form

from sqlalchemy.orm import Session

from pydantic import ValidationError

from db.repository.account import deposit_db, withdraw_db
from db.models.user import User
from db.repository.login import get_current_user
from db.session import get_db
from schemas.user import UserCreate
from db.repository.user import create_new_user

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/home")
async def home(request: Request):
    return templates.TemplateResponse("/bank/home.html", {"request": request})


@router.get("/profile") #returns profile page onle when user is logged in, need to fix
def profile(request: Request, user: User = Depends(get_current_user)):
    errors = []
    access_token = request.cookies.get("access_token")
    if not access_token or access_token == "": #exeption doesnt work
        return templates.TemplateResponse(
            "/auth/login.html",
            {"request": request, "errors": errors}
        )
    return templates.TemplateResponse(
        "/bank/profile.html",
        {"request": request, "user": user}
    )


@router.get("/deposit")
async def deposit(request: Request, user: User = Depends(get_current_user)):
    request.cookies.get("access_token")
    return templates.TemplateResponse("/bank/deposit.html", {"request": request, "user": user})

@router.post("/deposit")
async def deposit(request: Request, amount: int = Form(...), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user = deposit_db(id=user.id, amount=amount, db=db)
    return templates.TemplateResponse("/bank/profile.html", {"request": request, "user": user})


@router.get("/withdraw")
async def withdraw(request: Request, user: User = Depends(get_current_user)):
    request.cookies.get("access_token")
    return templates.TemplateResponse("/bank/withdraw.html", {"request": request, "user": user})


@router.post("/withdraw")
async def withdraw(request: Request, amount: int = Form(...), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    errors = []
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user = withdraw_db(id=user.id, amount=amount, db=db)
    return templates.TemplateResponse("/bank/profile.html", {"request": request, "user": user, "errors": errors})