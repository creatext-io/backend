import json
import re
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    status,
    APIRouter,
    Request,
    WebSocket,
    WebSocketDisconnect,
)
from sqlalchemy.orm import Session
from src.users.schemas import UserSchema
from src.database import get_db_session
from src.users.models import User

router = APIRouter()


@router.post("/login")
async def login(
    request: Request, schema: UserSchema, db: Session = Depends(get_db_session)
):

    # Get the text from client
    email = schema.email
    access_key = schema.key

    # TODO logic for validating email and access key for a user
    user = db.query(User).filter_by(email=email, access_key=access_key)

    user = list(user)[0]

    if user:
        # Send to GPT3 and get results
        return JSONResponse(
            content={
                "status": "successful",
                "message": "user successfuly logged in",
                "data": user.id,
            }
        )

    return JSONResponse(
        content={
            "status": "successful",
            "message": "user does not exist.",
            "data": None,
        }
    )


@router.post("/white-list-user")
async def whitelist_user(
    request: Request, schema: UserSchema, db: Session = Depends(get_db_session)
):

    # Get the text from client
    email = schema.email
    access_key = schema.key

    user = User(email=email, access_key=access_key)
    db.add(user)
    db.commit()

    if user:
        # Send to GPT3 and get results
        return JSONResponse(
            content={"message": "successful", "status": "user white listed."}
        )
