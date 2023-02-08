
import orjson
from fastapi import (APIRouter, Depends, Request
)
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.dashboard.schemas import DocumentSchema
from src.database import get_db_session
from src.editor.models import Document

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
            docs.append(orjson.loads(DocumentSchema.from_orm(doc).json()))

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


@router.get("/document/{doc_uuid}")
async def get_document(
    request: Request, doc_uuid: str, db: Session = Depends(get_db_session)
):

    # Get the document from db.
    document = list(db.query(Document).filter_by(doc_id=doc_uuid))

    if document:
        json_document = orjson.loads(DocumentSchema.from_orm(document[0]).json())
        return JSONResponse(
            content={
                "status": "successful",
                "message": "document fetched.",
                "data": [json_document],
            }
        )

    return JSONResponse(
        content={
            "status": "successful",
            "message": "No document",
            "data": [],
        }
    )


@router.post("/delete/{doc_id}")
async def delete_document(
    request: Request, doc_id: str, db: Session = Depends(get_db_session)
):

    # Delete the document
    db.query(Document).filter_by(doc_id=doc_id).delete()
    db.commit()

    return JSONResponse(
        content={
            "status": "successful",
            "message": "Document deleted",
        }
    )
