"""Pydantic schemas for request data"""
from pydantic import BaseModel, Json
from typing import Optional, Union
from datetime import datetime
import uuid


class AutoComplete(BaseModel):
    text: str
    multi_line: bool = False


class Search(BaseModel):
    query: str
    text: str


class DocumentSchema(BaseModel):
    title: str
    body: str
    date: Union[int, float]
