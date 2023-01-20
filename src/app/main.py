from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from src.app.core.config import settings
from src.editor import api as editor_apis
from src.users import api as user_apis
from src.dashboard import api as dashboard_apis


def get_application():
    _app = FastAPI(
        title=settings.PROJECT_NAME,
        redoc_url=None,
        openapi_url="/mIO83IT2Nj6SKPgwxT31ig/openapi.json",
        docs_url="/mIO83IT2Nj6SKPgwxT31ig/docs",
    )

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
app.include_router(user_apis.router)
app.include_router(dashboard_apis.router)

# Startup event is exceuted when app first starts/reloads
# @app.on_event("startup")
# async def startup():
#     print("hello world")
