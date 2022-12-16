"""Pydantic schemas for request data"""
from pydantic import BaseModel, Json
from typing import Optional


class AutoComplete(BaseModel):
    text: str
    multi_line: bool = False

class Search(BaseModel):
    query:str
    text: str
