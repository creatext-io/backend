""" This file has the DB settings """
import uuid
from contextlib import contextmanager
from datetime import datetime

import redis

# import redis
from sqlalchemy import BigInteger, Boolean, Column, DateTime, create_engine
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.app.core.config import settings

# Postgres db/password connection
SQLALCHEMY_DATABASE_URL = settings.DB_CONNECTION_URL


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


# SQLalchemy session object.
def get_db_session():
    """
    This is called everytime there is db related operation fastapi creates a Session (Depends object) (dependency injection)
    and `finally:` part is called when request/response cycle ends for a single request.
    (Read docs for more info)
    """

    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# SQLAlchemy transaction rollback context manager
@contextmanager
def atomic_transaction(*args, **kwargs):
    """
    This function ensures atomicity of a transaction so if any exception is raised during
    multi-level transactions then objects in memory will be rolled back without commting to DB.
    """
    session = kwargs.get("db")

    try:
        yield session
    except:
        session.rollback()
        raise

    else:
        session.commit()


class BaseModel(Base):
    """BaseModel for every children models"""

    __abstract__ = True

    id = Column(BigInteger, primary_key=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.now)
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_deleted = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<BaseModel: {self.uuid}>"


# Redis connection object


def redis_conn():
    try:
        redis_db = redis.Redis(
            host=settings.REDIS_HOSTNAME,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
        )
        if not redis_db.ping():
            raise Exception
    except Exception as e:
        redis_db = None

    return redis_db
