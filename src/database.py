""" This file has the DB settings """

from contextlib import contextmanager
from typing import final
# import redis
from sqlalchemy import create_engine
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


# Redis connection object
# try:
#     redis_db = redis.StrictRedis(host=settings.REDIS_HOST, port=6379)
# except:
#     redis_db = None

# try:
#     redis_user_param_db = redis.StrictRedis(host=settings.REDIS_HOST, port=6379, db=1)
# except:
#     redis_user_param_db = None


# def clear_redis_key(redis_db, key):
#     try:
#         redis_db.delete(key)
#     except Exception as e:
#         print(e)


# def set_redis_key(redis_db, key, val):
#     try:
#         if not key.startswith("store_"):
#             redis_db.set(key, val)
#         else:
#             redis_db.set(key, val, 28800)
#     except Exception as e:
#         print(e)


# def redis_get(redis_db, key):
#     try:
#         return redis_db.get(key)
#     except Exception as e:
#         print(e)
#         return None
