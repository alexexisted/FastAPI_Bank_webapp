from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi import responses, status, Form

from sqlalchemy.orm import Session

from pydantic import ValidationError

from db.models.user import User
from db.repository.login import get_current_user
from db.session import get_db
from schemas.user import UserCreate
from db.repository.user import create_new_user

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/home")
async def home(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("/bank/home.html", {"request": request})


@router.get("/profile")
async def check_profile(request: Request, user: User = Depends(get_current_user)):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return templates.TemplateResponse("/bank/profile.html", {"request": request, "user": user})
