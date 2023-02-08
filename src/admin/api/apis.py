from typing import Union
from fastapi import (APIRouter, Depends, Request
)
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.database import get_db_session, redis_conn
from src.editor.models import Document

router = APIRouter()


@router.get("/admin/token-analytics")
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

    elif not (doc_id and user_id):
        total_tokens = {}
        # Case when data is required for `all users and all documents`.
        docs = list(db.query(Document).all())

        for doc in docs:
            user_id = doc.user_id

            total_tokens[user_id] = {}
            # Get tokens consumed count from Redis for each document
            tokens_count = redis_db.hget(name=doc.doc_id, key="tokens_consumed")
            if tokens_count:
                total_tokens[user_id].update({doc.doc_id: int(tokens_count.decode())})

        return JSONResponse(content={"message": "successful", "data": total_tokens})

    else:
        return JSONResponse(content={"message": "successful", "data": ""})
