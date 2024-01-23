from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import Depends, APIRouter, HTTPException, status, Response, Request
from sqlalchemy.orm import Session
from datetime import timedelta
from jose import JWTError, jwt

from core.config import settings
from db.session import get_db
from core.hashing import Hasher
from db.repository.login import get_user, authenticate_user, get_token, get_current_user
from core.security import create_access_token
from schemas.token import Token
from db.models.user import User
from schemas.user import ShowUser

router = APIRouter()


@router.post("/login", response_model=Token)
def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db) #check if user exists
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.email}) #put the email as username to payload
    response.set_cookie("access_token", access_token, httponly=True) #set the token to cookie
    return {"access_token": access_token, "token_type": "bearer"}


@router.get('/protected', response_model=ShowUser)
async def info_user(request: Request, user: User = Depends(get_current_user)):
    access_token = request.cookies.get("access_token") #catch the token from cookie
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user
