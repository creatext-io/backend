from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

from src.database import Base, BaseModel

Base = declarative_base()


class Document(BaseModel):
    __tablename__ = "document"
    __mapper_args__ = {"polymorphic_identity": "document"}

    title = Column(String(500), unique=False, nullable=True)
    body = Column(Text(), nullable=True)
    date = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("user.id"))
    doc_id = Column(String(100), unique=True, nullable=True)

    def __repr__(self):
        return f"<Document: {self.id}>"
