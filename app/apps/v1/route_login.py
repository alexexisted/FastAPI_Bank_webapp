from fastapi import Depends, APIRouter, HTTPException, status, Response, Request, Form, responses
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session

from db.session import get_db

from db.repository.login import get_user, authenticate_user, get_token, get_current_user
from core.security import create_access_token
from schemas.token import Token
from db.models.user import User
from schemas.user import ShowUser

from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.post("/login") #tackled
async def login(
        request: Request,
        email: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)):
    errors = []
    user = authenticate_user(email=email, password=password, db=db)
    if not user:
        errors.append("Incorrect email or password")
        return templates.TemplateResponse("auth/login.html", {"request": request, "errors": errors})
    access_token = create_access_token(data={"sub": email})
    response = responses.RedirectResponse(
        "/profile", status_code=status.HTTP_302_FOUND
    )
    response.set_cookie("access_token", access_token, httponly=True)
    return response


@router.get('/logout')
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"status": "successfully logged out"} #need to make alert for a main page


@router.get('/registration')
async def registration(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})

