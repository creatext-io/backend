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


@router.get("/documents")
async def get_all_documents(request: Request, db: Session = Depends(get_db_session)):

    # Fetch the document from db.
    documents = list(db.query(Document).filter(Document.id >= 1))

    # TODO for each document in list `documents` send the document data find out
    # how to do it in an optimised manner using pydantic from_orm()

    if documents:
        return JSONResponse(
            content={"message": "successful", "status": "documents fetched."}
        )
