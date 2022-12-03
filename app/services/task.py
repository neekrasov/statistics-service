import uuid
from datetime import datetime

from ..schemas.task import TaskIn, TaskInDB, TaskStatus, Task
from ..db.dao.task import TaskDao


class TaskService:
    def __init__(self, task_dao: TaskDao):
        self._task_dao = task_dao

    async def create_task(self, in_scheme: TaskIn):
        obj_in_db = TaskInDB(
            **in_scheme.dict(),
            id=uuid.uuid4(),
            created_at=datetime.utcnow(),
        )
        task_obj = await self._task_dao.save(obj_in_db)
        await self._task_dao.commit()
        return Task.from_orm(task_obj)

    async def get_task_by_id(self, id: int) -> Task:
        task = await self._task_dao.get(id=id)
        return Task.from_orm(task) if task else None

    async def get_task_by_search_phrase(self, search_phrase: str) -> Task:
        task = await self._task_dao.get(search_phrase=search_phrase)
        return Task.from_orm(task) if task else None

    async def _toggle_task(self, task: Task, task_status: TaskStatus) -> Task:
        updated_task = await self._task_dao.update(
            obj_in={"status": task_status}, id=str(task.id)
        )
        await self._task_dao.commit()
        return updated_task

    async def disable_task(self, task: Task) -> Task:
        return await self._toggle_task(task, TaskStatus.STOPPED)

    async def enable_task(self, task: Task) -> Task:
        return await self._toggle_task(task, TaskStatus.RUNNING)

    async def check_task_status(
        self,
        task: Task,
        expected_status: str,
    ) -> bool:
        return task.status != expected_status
