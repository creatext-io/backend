"""Pydantic schemas for User apis"""
from pydantic import BaseModel, Json
from typing import Optional


class UserSchema(BaseModel):
    email: str
    key: str
