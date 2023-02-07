import httpx
import asyncio
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
from ..schemas import AutoComplete, Search, AutoCompleteNew
from ...openai.gpt3 import GPT3
from ...openai.functions import auto_completions
from ...cohere.semantic_search import semantic_search
from sqlalchemy.orm import Session
from src.database import get_db_session
from src.editor.schemas import DocumentSchema
from src.editor.models import Document
from datetime import datetime
from src.database import redis_conn
from src.openai import auto_complete_engine, auto_completions
from sse_starlette.sse import EventSourceResponse


router = APIRouter()


@router.get("/")
def get_editor():
    return "Hold your horses! This is the root"


@router.post("/auto-complete")
async def auto_complete(request: Request, schema: AutoComplete):

    # Get the text from client
    text = schema.text

    # Send to GPT3 and get results
    gpt3_output = auto_completions(text, multi_line=schema.multi_line)
    return JSONResponse(
        content={"message": "successful", "input_data": text, "completion": gpt3_output}
    )


@router.post("/autocomplete")
async def auto_complete(
    request: Request, schema: AutoCompleteNew, redis_db=Depends(redis_conn)
):

    # Get the request data from client
    document_id = schema.doc_id
    text = schema.text
    cursor_position = schema.cursor_position

    # Form a context window in Redis and then call gpt3 and maintain the document window in Redis only.
    # auto_completion = auto_complete_engine(
    #     data=text, redis=redis_db, doc_id=document_id
    # )

    auto_completion = auto_completions(data=text, redis=redis_db, doc_id=document_id)

    return JSONResponse(content={"status": "successful", "completion": auto_completion})


@router.post("/search")
async def search(request: Request, schema: Search):
    """Performs a semantic searh over text"""

    # Pre-process text and slice it into chunks.
    # Here we split the text based on newline characters.

    # ~~~ Code when receiving text with <p></p> tags. ~~~~
    # Use regex to parse for <p> tags
    # p_tag = re.finditer("<p>",schema.text)
    # p_slash_tag = re.finditer("</p>",schema.text)

    # pattern_list = {"p":[p_tag],"/p":[p_slash_tag]}
    # for key,match_obj in pattern_list.items():
    #     pattern_list[key]=[match_p.span() for match_p in match_obj[0]]

    # # Now merge the two lists in using regex
    # final_list = []
    # for list in pattern_list.values():
    #     final_list.extend(list)

    # # Sort the matches
    # final_list.sort()

    # # Prepare paragraphs for semantic search
    # documents_list = []

    # for index in range(0,len(final_list),2):
    #     # Every even index is starting index of paragrah and odd index is ending index
    #     doc = schema.text[final_list[index][1]:final_list[index+1][0]]
    #     documents_list.append(doc)

    # ~~~ Without <p></p> tags logic. ~~~

    documents_list = schema.text.split("\n")

    # Remove the last element from list if it's an empty string with '\n' char
    if not documents_list[-1]:
        documents_list.pop()

    search_results = semantic_search(query=schema.query, documents=documents_list)

    return JSONResponse(
        content={"message": "successful", "search_results": search_results}
    )


@router.put("/save")
async def save_document(
    request: Request, schema: DocumentSchema, db: Session = Depends(get_db_session)
):

    title = schema.title
    body = schema.body
    unix_date = schema.date
    user = schema.user_id
    doc_id = schema.doc_id

    # Fetch the documet if not present in db then create one.
    document = list(db.query(Document).filter_by(doc_id=doc_id))

    if document:
        document[0].body = body
        document[0].date = datetime.fromtimestamp(unix_date)
        document[0].title = title
        db.commit()

    else:
        document = Document(
            title=title,
            body=body,
            date=datetime.fromtimestamp(unix_date),
            user_id=user,
            doc_id=doc_id,
        )
        db.add(document)
        db.commit()

    return JSONResponse(content={"status": "successful", "message": "document saved"})


@router.get("/stream-autocomplete")
async def auto_complete(request: Request, data: str, redis_db=Depends(redis_conn)):

    # TODO convert this endpoint to POST this is for testing only.

    stop_sequences = ["###", "##", "\n\n\n"]
    prompt_template = "Provide text completion for the following incomplete sentences if there is no starting sentence then create one of its own based on what is written before.\n\n{0}".format(
        data
    )

    async def streamer():
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                url="https://api.openai.com/v1/completions",
                headers={
                    "Authorization": "Bearer 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"
                },
                json={
                    "model": "text-davinci-003",
                    "prompt": prompt_template,
                    "max_tokens": 50,
                    "temperature": 0.7,
                    "stop": stop_sequences,
                    "stream": True,
                },
            ) as responser:
                async for chunk in responser.aiter_text():
                    yield chunk
                    await asyncio.sleep(0.3)

    return EventSourceResponse(streamer())
