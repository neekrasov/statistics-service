from fastapi import FastAPI
from .providers import (
    provide_session,
    provide_task_service,
    provide_statistics_service,
    provide_scheduler_service,
)

from .stubs import (
    provide_session_stub,
    provide_task_service_stub,
    provide_stat_service_stub,
    provide_worker_channel_stub,
    provide_scheduler_service_stub,
)

from app.worker.client_provider import provide_worker_channel


async def setup_di(app: FastAPI) -> None:
    context_session = provide_session()

    app.dependency_overrides = {
        provide_session_stub: context_session,
        provide_task_service_stub: provide_task_service,
        provide_stat_service_stub: provide_statistics_service,
        provide_worker_channel_stub: provide_worker_channel,
        provide_scheduler_service_stub: provide_scheduler_service,
    }
