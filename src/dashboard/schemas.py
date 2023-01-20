"""Pydantic schemas for Dashboard apis"""
from pydantic import BaseModel, Json
from typing import Optional
from datetime import datetime
import uuid


class DocumentSchema(BaseModel):
    id: Optional[int]
    uuid: Optional[uuid.UUID]
    created_at: Optional[datetime]
    modified_at: Optional[datetime]
    is_deleted: Optional[bool]
    is_active: Optional[bool]
    title: str
    body: str
    date: Optional[datetime]

    class Config:
        orm_mode = True
