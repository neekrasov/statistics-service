import uuid
import asyncio
from datetime import datetime
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.core.di.providers import provide_statistics_service
from app.db.models import Task, TaskStatus
from app.db.dao import StatisticsDao
from app.worker.parser import parser
from app.schemas.statistics import StatisticsInDB, Statistics
from app.core.settings import get_settings

settings = get_settings()


async def add_task_to_scheduler(
    task_obj: Task,
    session: AsyncSession,
    scheduler: AsyncIOScheduler,
    timeout: int
) -> tuple[uuid.UUID, str]:

    scheduler.add_job(
        create_statistics,
        id=str(task_obj.id),
        minutes=timeout,
        args=(task_obj, session),
        trigger="interval",
    )


async def create_statistics(
    task_obj: Task,
    session: AsyncSession
) -> Statistics:

    records_count: int = await parser(
        task_obj.search_phrase, url=settings.parse_url
    )
    stat_service = provide_statistics_service(StatisticsDao(session))
    stat_obj = await stat_service.create_statistics(
        StatisticsInDB(
            task_id=task_obj.id,
            records_count=records_count,
            created_at=datetime.utcnow(),
        )
    )
    return stat_obj


async def start_tasks(
    contextsession: sessionmaker,
    scheduler: AsyncIOScheduler,
    timeout: int
) -> None:

    async with contextsession() as session:
        tasks = await session.execute(
            select(Task).filter(Task.status == TaskStatus.RUNNING)
        )

    tasks_list = []
    for task in tasks.scalars().all():
        async with contextsession() as session:
            tasks_list.append(
                add_task_to_scheduler(
                    task_obj=task,
                    session=session,
                    scheduler=scheduler,
                    timeout=timeout,
                )
            )
    await asyncio.gather(*tasks_list)
