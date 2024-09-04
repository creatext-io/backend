from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from src.database import BaseModel


class Feedback(BaseModel):
    __tablename__ = "feedback"
    __mapper_args__ = {"polymorphic_identity": "feedback"}

    text = Column(Text(), nullable=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    date = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Feedback: {self.id}>"
