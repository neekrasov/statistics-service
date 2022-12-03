from typing import Callable, Type
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import get_settings
from app.db.base import async_session
from app.db.dao import BaseDAO, TaskDao, StatisticsDao
from app.services import TaskService, StatisticsService, SchedulerService

from .stubs import provide_session_stub, provide_worker_channel_stub
from grpc.aio import Channel


def provide_session():
    return async_session(get_settings().postgres_uri)


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
