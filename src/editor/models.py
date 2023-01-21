import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    JSON,
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from src.database import BaseModel

from src.database import Base


Base = declarative_base()


class Document(BaseModel):
    __tablename__ = "document"
    __mapper_args__ = {"polymorphic_identity": "document"}

    title = Column(String(500), unique=False, nullable=True)
    body = Column(Text(), nullable=True)
    date = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("user.id"))

    def __repr__(self):
        return f"<Document: {self.id}>"
