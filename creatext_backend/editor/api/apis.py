from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_editor():
    return "editor app created!"
