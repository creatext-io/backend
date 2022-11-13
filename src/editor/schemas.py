"""Pydantic schemas for request data"""
from pydantic import BaseModel, Json
from typing import Optional


class AutoComplete(BaseModel):
    text: str

class Search(BaseModel):
    query:str
    text: str