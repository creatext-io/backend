from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src.utils.dependencies import verify_password, create_access_token
from src.auth.schemas import User
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from src.database import get_db_session
from src.users.models import User
from fastapi.responses import JSONResponse
from src.utils.dependencies import get_password_hash

router = APIRouter()


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db_session),
):

    # Validate if user with this email exists in DB
    user = db.query(User).filter_by(email=form_data.username)
    user = list(user)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = user[0]

    # Check for text password against hashed password stored in DB
    password_match = verify_password(form_data.password, user.access_key)

    if not password_match:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create JWT token for the user
    jwt_token = create_access_token(data={"sub": user.email})
    return JSONResponse(
        content={
            "status": "successful",
            "message": "user successfuly logged in",
            "data": jwt_token,
        }
    )


@router.post("/signup")
async def signup(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db_session),
):

    email = form_data.username
    access_key = form_data.password

    # Save the email and password (after hasing) in DB and create a User.

    hashed_access_key = get_password_hash(access_key)

    # Check if user already exists in DB with same username
    user_exists_query = db.query(User).filter_by(email=email).exists()
    user_exists = db.query(user_exists_query).scalar()

    if not user_exists:
        user = User(email=email, access_key=hashed_access_key)
        db.add(user)
        db.commit()

        return JSONResponse(
            content={
                "status": "successful",
                "message": "user successfuly signed up",
                "data": "",
            }
        )

    return JSONResponse(
        content={
            "status": "successful",
            "message": "user with this email already exists",
            "data": "",
        }
    )
