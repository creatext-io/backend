from typing import Union
from pydantic import BaseModel


class User(BaseModel):
    email: Union[str, None] = None
    is_active: Union[bool, None] = None
