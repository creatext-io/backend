from typing import Union

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.database import get_db_session, redis_conn
from src.editor.models import Document
from src.users.models import User
from src.users.schemas import UserSchema

router = APIRouter(prefix="/admin")


@router.get("/token-analytics")
async def auto_complete(
    request: Request,
    user_id: Union[int, None] = None,
    doc_id: Union[str, None] = None,
    db: Session = Depends(get_db_session),
    redis_db=Depends(redis_conn),
):
    """
    This endpoint fetches all the tokens consumed for each user or
    for each document or all users and all documents.
    TODO refine as per requirements.
    """

    # Query the DB for a given user/document or fetch all data across all users if no query params
    if user_id:
        total_tokens = {user_id: {}}
        docs = list(db.query(Document).filter_by(user_id=user_id))

        for doc in docs:
            # Get tokens consumed count from Redis for each document
            tokens_count = redis_db.hget(name=doc.doc_id, key="tokens_consumed")
            if tokens_count:

                total_tokens[user_id].update(
                    {str(doc.doc_id): int(tokens_count.decode())}
                )

        return JSONResponse(content={"message": "successful", "data": total_tokens})

    elif doc_id:
        total_tokens = {doc_id: None}

        # Get tokens consumed count from Redis for each document
        tokens_count = redis_db.hget(name=doc_id, key="tokens_consumed")
        if tokens_count:

            total_tokens[doc_id] = int(tokens_count.decode())
            return JSONResponse(content={"message": "successful", "data": total_tokens})

    else:
        total_tokens = {}
        # Case when data is required for `all users and all documents`.
        docs = list(db.query(Document).all())

        for doc in docs:
            user_id = doc.user_id

            if user_id not in total_tokens.keys():
                total_tokens[user_id] = {}

            # Get tokens consumed count from Redis for each document
            tokens_count = redis_db.hget(name=doc.doc_id, key="tokens_consumed")

            if tokens_count:
                total_tokens[user_id].update({doc.doc_id: int(tokens_count.decode())})

        return JSONResponse(content={"message": "successful", "data": total_tokens})


@router.post("/whitelist-user")
async def whitelist_user(
    request: Request, schema: UserSchema, db: Session = Depends(get_db_session)
):

    # Get the text from client
    email = schema.email
    access_key = schema.key

    user = User(email=email, access_key=access_key)
    db.add(user)
    db.commit()

    if user:
        # Send to GPT3 and get results
        return JSONResponse(
            content={"message": "user white listed.", "status": "successful"}
        )
