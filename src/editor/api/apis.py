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
from ...openai.functions import auto_completions

router = APIRouter()


@router.get("/")
def get_editor():
    return "editor app created!"


@router.post("/auto-complete")
async def auto_complete(request: Request, schema: AutoComplete):

    # Get the text from client
    text = schema.text

    # Send to GPT3 and get results
    gpt3_output = auto_completions(text)
    return JSONResponse(
        content={"message": "successful", "input_data": text, "completion": gpt3_output}
    )
