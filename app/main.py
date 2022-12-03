from fastapi import FastAPI
from app.api.router import router
from app.core.settings import get_settings
from app.core.di.setup import setup_di


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.title, description=settings.descriprion)

    async def startup():
        return await setup_di(app)

    app.add_event_handler("startup", startup)
    app.include_router(router)

    return app


app = create_app()
