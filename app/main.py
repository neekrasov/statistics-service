from fastapi import FastAPI
from .api.router import router
from .core.settings import get_settings
from .services.scheduler import on_startup_sheduler_handler

def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.title, description=settings.descriprion)
    app.add_event_handler("startup", on_startup_sheduler_handler)
    app.include_router(router)
    return app


app = create_app()