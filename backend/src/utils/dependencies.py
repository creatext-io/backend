from passlib.context import CryptContext
from jose import JWTError, jwt
from typing import Union
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pydantic import BaseModel
import os
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.auth.schemas import User
from sqlalchemy.orm import Session
from src.database import get_db_session
from src.users.models import User

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")


class Token(BaseModel):
    access_token: str
    token_type: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenData(BaseModel):
    email: Union[str, None] = None


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# async def get_current_user(
#     token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_session)
# ):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
#         email: str = payload.get("sub")
#         if email is None:
#             raise credentials_exception
#         token_data = TokenData(email=email)
#     except JWTError:
#         raise credentials_exception

#     user = db.query(User).filter_by(email=token_data.email)
#     user = list(user)[0]

#     if not user:
#         raise credentials_exception
#     return user


# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if not current_user.is_active:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


async def authenticate_jwt_token(token: str = Depends(oauth2_scheme)):
    """
    This dependency checks internally for a valid Authorization header using FastAPI's `OAuth2PasswordBearer`
    and gives the token attached to the auth header then we decode the jwt and get the user's email.

    This is fast validation of JWT token however each URL route can fetch the rspective `User` object associated
    with the user email from DB as this behaviour is not default because it slows the API.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:

        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception

    return email
