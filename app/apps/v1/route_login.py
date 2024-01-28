import json
from fastapi import Depends, APIRouter, status, Response, Request, Form, responses
from sqlalchemy.orm import Session

from db.session import get_db

from db.repository.login import authenticate_user
from core.security import create_access_token
from db.repository.user import create_new_user
from schemas.user import UserCreate

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


@router.get('/logout') #fixed
async def logout(request: Request, response: Response):
    errors = []
    errors.append("Successfully logged out")
    response = templates.TemplateResponse("bank/redirect_to_login.html", {"request": request, "errors": errors})
    response.delete_cookie(key="access_token", httponly=True)
    return response

@router.get('/registration')
async def registration(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})


@router.post('/registration')
async def registration(request: Request,
                       name: str = Form(...),
                       surname: str = Form(...),
                       email: str = Form(...),
                       password: str = Form(...),
                       db: Session = Depends(get_db)):
    errors = []
    try:
        user = UserCreate(name=name, surname=surname, email=email, password=password)
        create_new_user(user=user, db=db)
        errors.append("Successfully registered, now you can login")
        return responses.RedirectResponse("/login", status_code=status.HTTP_302_FOUND)
    except ValidationError as e:
        errors = json.loads(e.json())
        for item in errors:
            errors.append(item.get("loc")[0] + ':' + item.get("msg"))
    return templates.TemplateResponse(
        "auth/register.html", {"request": request, "errors": errors}
    )





