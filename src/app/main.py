from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.app.core.config import settings
from src.editor import api as editor_apis


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME,docs_url="/mIO83IT2Nj6SKPgwxT31ig/docs",redoc_url=None,openapi_url=None)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


app = get_application()


# Include all API urls from different modules
app.include_router(editor_apis.router)
