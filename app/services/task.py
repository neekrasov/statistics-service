import uuid
from datetime import datetime

from sqlalchemy import false

from ..schemas.task import TaskIn, TaskInDB, TaskStatus
from ..db.dao.task import TaskDao
from ..db.models import Task

async def create_task(in_scheme: TaskIn, task_dao: TaskDao):
    obj_in_db = TaskInDB(
        **in_scheme.dict(),
        id = uuid.uuid4(),
        created_at = datetime.utcnow(),
    )
    task_obj = await task_dao.save(obj_in_db)
    await task_dao.commit()
    return task_obj

async def get_all_tasks(task_dao: TaskDao) -> list[Task]:
    task_objects = await task_dao.get_many(limit=100)
    return task_objects

async def get_task_by_id(id: int, task_dao: TaskDao) -> Task:
    task = await task_dao.get(id=id)
    return task

async def get_task_by_search_phrase(search_phrase: str, task_dao: TaskDao) -> Task:
    task = await task_dao.get(search_phrase=search_phrase)
    return task

async def _toggle_task(task: Task, task_dao: TaskDao, task_status: TaskStatus)-> Task:
    updated_task = await task_dao.update(obj_in={"status": task_status}, db_obj=task)
    await task_dao.commit()
    return updated_task

async def disable_task(task: Task, task_dao: TaskDao)-> Task:
    return await _toggle_task(task, task_dao, TaskStatus.STOPPED)
    
async def enable_task(task: Task, task_dao: TaskDao)-> Task:
    return await _toggle_task(task, task_dao, TaskStatus.RUNNING)

async def check_task_status(task: Task, expected: str) -> bool:
    if task.status != expected:
        return false