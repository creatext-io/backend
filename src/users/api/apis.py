from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.admin.models import Feedback
from src.database import get_db_session
from src.users.models import User
from src.users.schemas import FeedbackSchema, UserSchema
from src.utils.dependencies import authenticate_jwt_token


router = APIRouter()


@router.post("/feedback")
async def collect_feedback(
    request: Request,
    schema: FeedbackSchema,
    db: Session = Depends(get_db_session),
    email: str = Depends(authenticate_jwt_token),
):
    user = list(db.query(User).filter_by(email=email))[0]
    feedback_obj = Feedback(text=schema.text, user_id=user.id)
    db.add(feedback_obj)
    db.commit()

    return JSONResponse(
        content={"status": "successful", "message": "Feedback submitted"}
    )
