from typing import Callable, Type

from fastapi import Depends
from grpc.aio import Channel
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import async_session
from app.db.dao import BaseDAO, StatisticsDao, TaskDao
from app.services import SchedulerService, StatisticsService, TaskService
from app.worker.client_provider import provide_worker_channel  # noqa

from .stubs import provide_session_stub, provide_worker_channel_stub


def provide_session(uri: str):
    return async_session(uri)


def get_dao(
    repo_type: Type[BaseDAO],
) -> Callable[[AsyncSession], BaseDAO]:
    def _get_dao(
        session: AsyncSession = Depends(provide_session_stub),
    ) -> BaseDAO:
        return repo_type(session)

    return _get_dao


def provide_task_service(
    task_dao: TaskDao = Depends(get_dao(TaskDao)),
) -> TaskService:
    return TaskService(task_dao)


def provide_statistics_service(
    statistics_dao: StatisticsDao = Depends(get_dao(StatisticsDao)),
) -> StatisticsService:
    return StatisticsService(statistics_dao)


def provide_scheduler_service(
    channel: Channel = Depends(provide_worker_channel_stub),
) -> SchedulerService:
    return SchedulerService(channel)
