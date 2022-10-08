import json
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
from ..schemas import AutoComplete
from ...openai.gpt3 import GPT3

router = APIRouter()


@router.get("/")
def get_editor():
    return "editor app created!"


@router.post("/auto-complete")
async def auto_complete(request: Request, schema: AutoComplete):

    # Get the text from client
    text = schema.text

    # Send to GPT3 and get results
    gpt3_instance = GPT3()
    return JSONResponse(content={"message": "successful", "data": text})
