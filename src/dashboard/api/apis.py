import json
import re
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    status,
    APIRouter,
    Request,
    WebSocket,
    WebSocketDisconnect,
)
from sqlalchemy.orm import Session
from src.database import get_db_session

from src.editor.models import Document
from src.dashboard.schemas import DocumentSchema

router = APIRouter()


@router.get("/documents/{user_id}")
async def get_all_documents(
    request: Request, user_id: int, db: Session = Depends(get_db_session)
):

    # Fetch the document from db.
    documents = list(db.query(Document).filter_by(user_id=user_id))

    if documents:
        docs = []

        # Form data objects
        for doc in documents:
            docs.append(DocumentSchema.from_orm(doc).json())

        return JSONResponse(
            content={
                "message": "successful",
                "status": "documents fetched.",
                "data": docs,
            }
        )
    else:
        return JSONResponse(
            content={
                "message": "successful",
                "status": "documents fetched.",
                "data": [],
            }
        )
