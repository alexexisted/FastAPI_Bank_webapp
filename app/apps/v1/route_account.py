from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi import responses, status, Form

from sqlalchemy.orm import Session

from db.repository.account import deposit_db, withdraw_db
from db.models.user import User
from db.repository.login import get_current_user
from db.session import get_db


templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/home")
async def home(request: Request):
    return templates.TemplateResponse("/bank/home.html", {"request": request})


@router.get("/unauthenticated")
async def unauthenticated(request: Request):
    return templates.TemplateResponse("bank/redirect_to_login.html", {"request": request})


@router.get("/profile")
async def profile(request: Request, db: Session = Depends(get_db)):
    try:
        token = request.cookies.get("access_token")
        user = get_current_user(token=token, db=db)
        return templates.TemplateResponse("/bank/profile.html", {"request": request, "user": user})
    except Exception:
        return responses.RedirectResponse(
            "/unauthenticated", status_code=status.HTTP_302_FOUND
        )


@router.get("/deposit")
async def deposit(request: Request, db: Session = Depends(get_db)):
    try:
        token = request.cookies.get("access_token")
        user = get_current_user(token=token, db=db)
        return templates.TemplateResponse("/bank/deposit.html", {"request": request, "user": user})
    except Exception:
        return responses.RedirectResponse(
            "/unauthenticated", status_code=status.HTTP_302_FOUND
        )


@router.post("/deposit")
async def deposit(request: Request, amount: int = Form(...), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user = deposit_db(id=user.id, amount=amount, db=db)
    return templates.TemplateResponse("/bank/profile.html", {"request": request, "user": user})


@router.get("/withdraw")
async def withdraw(request: Request, db: Session = Depends(get_db)):
    try:
        token = request.cookies.get("access_token")
        user = get_current_user(token=token, db=db)
        return templates.TemplateResponse("/bank/withdraw.html", {"request": request, "user": user})
    except Exception:
        return responses.RedirectResponse(
            "/unauthenticated", status_code=status.HTTP_302_FOUND
        )


@router.post("/withdraw")
async def withdraw(request: Request, amount: int = Form(...), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    errors = []
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user = withdraw_db(id=user.id, amount=amount, db=db)
    return templates.TemplateResponse("/bank/profile.html", {"request": request, "user": user, "errors": errors})
