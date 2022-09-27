from typing import Tuple
import uuid
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from ..schemas.statistics import StatisticsInDB
from ..db.dao.statistics import StatisticsDao
from ..db.dao.task import TaskDao
from ..db.models.statistics import Statistics
from ..db.models.task import TaskStatus
from ..db.base import get_session
from .statistics import create_statistics
from .parser import parser
from .task import get_all_tasks, disable_task
from ..db.models import Task


scheduler = AsyncIOScheduler()

async def add_task_to_scheduler(
    task_obj: Task,
    dao: StatisticsDao,
    trigger: str = 'interval',
    **kwargs) -> Tuple[uuid.UUID, str]:
    
    uuid_ = task_obj.id
    search_phrase = task_obj.search_phrase
    
    async def job():
        return await _create_search_task(task_obj, dao)
    
    scheduler.add_job(job, trigger, id=str(uuid_), seconds=10, **kwargs)
    return (uuid_, search_phrase)


async def _create_search_task(task_obj: Task, stat_dao: StatisticsDao) -> Statistics:
    records_count = await parser(task_obj.search_phrase)
    obj_in_db = StatisticsInDB(
        task_id=task_obj.id,
        records_count=records_count,
        created_at=datetime.utcnow()
    )
    stat_obj = await create_statistics(obj_in_db, stat_dao)
    return stat_obj

async def remove_task(task: Task, task_dao: TaskDao) -> None:
    scheduler.remove_job(str(task.id))
    await disable_task(task, task_dao=task_dao)

async def on_startup_sheduler_handler():
    session_gen2 = get_session()
    async_session2 = await anext(session_gen2)
    task_dao = TaskDao(async_session2)
    
    task_objects = await get_all_tasks(task_dao)

    for task_obj in task_objects:
        if task_obj.status == TaskStatus.RUNNING:
            session_gen = get_session()
            async_session = await anext(session_gen)
            await add_task_to_scheduler(task_obj=task_obj, dao=StatisticsDao(async_session))
    
    scheduler.start()
    
    