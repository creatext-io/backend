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
from ..schemas import AutoComplete,Search
from ...openai.gpt3 import GPT3
from ...openai.functions import auto_completions
from ...cohere.semantic_search import semantic_search


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


@router.post("/search")
async def search(request: Request, schema: Search):
    """Performs a semantic searh over text"""

    # Pre-process text and slice it into chunks.
    # Here we split the text based on newline characters.


    # ~~~ Code when receiving text with <p></p> tags. ~~~~
    # # Use regex to parse for <p> tags
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

    documents_list = schema.text.split("\n")
    search_results = semantic_search(query=schema.query,documents=documents_list)

    return JSONResponse(content={"message": "successful", "search_results": search_results})
