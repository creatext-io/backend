from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from src.admin import api as admin_apis
from src.app.core.config import settings
from src.dashboard import api as dashboard_apis
from src.editor import api as editor_apis
from src.users import api as user_apis
from src.auth import api as auth_apis
from src.utils.dependencies import authenticate_jwt_token


def get_application():

    if not settings.DEVELOPMENT:
        import sentry_sdk

        sentry_sdk.init(
            dsn="https://733541db08294a60a49d62d2a0ab7840@o4504547672588288.ingest.sentry.io/4504547676323840",
            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            # We recommend adjusting this value in production,
            traces_sample_rate=0.5,
        )

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
app.include_router(
    editor_apis.router
)  # ,dependencies=[Depends(authenticate_jwt_token)])
app.include_router(user_apis.router)  # ,dependencies=[Depends(authenticate_jwt_token)])
app.include_router(
    dashboard_apis.router
)  # ,dependencies=[Depends(authenticate_jwt_token)])
app.include_router(admin_apis.router)
app.include_router(auth_apis.router)


# Startup event is exceuted when app first starts/reloads
# @app.on_event("startup")
# async def startup():
#     print("hello world")
