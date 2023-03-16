import orjson
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.dashboard.schemas import DocumentSchema
from src.database import get_db_session
from src.editor.models import Document
from src.users.models import User
from src.utils.dependencies import authenticate_jwt_token


router = APIRouter()


@router.get("/documents")
async def get_all_documents(
    request: Request,
    db: Session = Depends(get_db_session),
    email: str = Depends(authenticate_jwt_token),
):

    user = list(db.query(User).filter_by(email=email))

    user = user[0]
    # Fetch the document from db.
    documents = list(db.query(Document).filter_by(user_id=user.id))

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
    request: Request,
    doc_uuid: str,
    db: Session = Depends(get_db_session),
    email: str = Depends(authenticate_jwt_token),
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
    request: Request,
    doc_id: str,
    db: Session = Depends(get_db_session),
    email: str = Depends(authenticate_jwt_token),
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
