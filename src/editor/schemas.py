"""Pydantic schemas for request data"""
from typing import Union, Optional

from pydantic import BaseModel


class AutoComplete(BaseModel):
    text: str
    multi_line: bool = False


class AutoCompleteNew(BaseModel):
    doc_id: str
    text: str
    cursor_position: int


class Search(BaseModel):
    query: str
    text: str


class DocumentSchema(BaseModel):
    title: str
    body: str
    date: Union[int, float]
    user_id: Optional[int]
    doc_id: str
