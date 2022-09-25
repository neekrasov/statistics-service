import uuid
from datetime import datetime

from ..schemas.task import TaskIn, TaskInDB
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