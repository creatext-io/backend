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
    title: str
    body: str
    date: Optional[datetime]
    doc_id: str

    class Config:
        orm_mode = True
