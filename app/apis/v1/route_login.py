from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from jose import JWTError, jwt

from core.config import settings
from db.session import get_db
from core.hashing import Hasher
from db.repository.login import get_user, authenticate_user
from core.security import create_access_token
from schemas.token import Token

router = APIRouter()


@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.email}) #put the email as username to payload
    return {"access_token": access_token, "token_type": "bearer"}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )

    try:
        # decode token to get the email from payload
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub") #get the email as username from token's payload
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(email=username, db=db) #get the user by email using get_user function
    if user is None:
        raise credentials_exception
    return user
