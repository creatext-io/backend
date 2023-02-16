from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.admin.models import Feedback
from src.database import get_db_session
from src.users.models import User
from src.users.schemas import FeedbackSchema, UserSchema

router = APIRouter()


@router.post("/login")
async def login(
    request: Request,
    schema: UserSchema,
    db: Session = Depends(get_db_session),
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


@router.post("/feedback")
async def collect_feedback(
    request: Request, schema: FeedbackSchema, db: Session = Depends(get_db_session)
):

    feedback_obj = Feedback(text=schema.text, user_id=schema.user_id)
    db.add(feedback_obj)
    db.commit()

    return JSONResponse(
        content={"status": "successful", "message": "Feedback submitted"}
    )
