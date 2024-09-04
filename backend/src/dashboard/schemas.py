"""Pydantic schemas for Dashboard apis"""
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


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
