from fastapi import FastAPI
from .api.router import router
from .core.settings import get_settings

def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.title, description=settings.descriprion)
    app.include_router(router)
    return app


app = create_app()
