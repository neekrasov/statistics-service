from fastapi import FastAPI

from app.core.settings import Settings

from .providers import (
    async_session,
    provide_task_service,
    provide_statistics_service,
    provide_scheduler_service,
    provide_worker_channel,
)

from .stubs import (
    provide_session_stub,
    provide_task_service_stub,
    provide_stat_service_stub,
    provide_worker_channel_stub,
    provide_scheduler_service_stub,
)


def setup_di(app: FastAPI, settings: Settings) -> None:
    context_session = async_session(settings.postgres_uri)

    app.dependency_overrides = {
        provide_session_stub: context_session,
        provide_task_service_stub: provide_task_service,
        provide_stat_service_stub: provide_statistics_service,
        provide_worker_channel_stub: provide_worker_channel,
        provide_scheduler_service_stub: provide_scheduler_service,
    }
