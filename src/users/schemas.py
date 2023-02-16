"""Pydantic schemas for User apis"""

from pydantic import BaseModel


class UserSchema(BaseModel):
    email: str
    key: str


class FeedbackSchema(BaseModel):
    text: str
    user_id: int
