from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from app.api.router import router
from app.core.settings import get_settings
from app.core.di.setup import setup_di


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.title,
        description=settings.descriprion,
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
        default_response_class=ORJSONResponse,
    )
    setup_di(app, settings)
    app.include_router(router)

    return app


app = create_app()
