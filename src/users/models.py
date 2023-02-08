
from sqlalchemy import (Column, String
)
from sqlalchemy.orm import relationship

from src.database import BaseModel

# class BaseModel(Base):
#     """BaseModel for every children models"""

#     __abstract__ = True

#     id = Column(BigInteger, primary_key=True)
#     uuid = Column(UUID(as_uuid=True), default=uuid.uuid4)
#     created_at = Column(DateTime, default=datetime.now)
#     modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
#     is_deleted = Column(Boolean, default=False)
#     is_active = Column(Boolean, default=True)

#     def __repr__(self):
#         return f"<BaseModel: {self.uuid}>"


class User(BaseModel):
    __tablename__ = "user"
    __mapper_args__ = {"polymorphic_identity": "user"}

    email = Column(String(200), unique=True)
    access_key = Column(String(200), nullable=True)
    documents = relationship("Document", backref="documents")

    def __repr__(self):
        return f"<User: {self.id}>"
