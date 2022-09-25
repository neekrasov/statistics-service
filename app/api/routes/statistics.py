from datetime import datetime
import uuid
from fastapi import APIRouter, Depends

from ...schemas.task import TaskIn
from ...db.dao import TaskDao, StatisticsDao
from ...services.scheduler import add_task_to_scheduler
from ..dependencies.task import get_task_dao
from ..dependencies.statistics import get_stat_dao
from ...services.task import create_task

router = APIRouter(prefix='', tags=['statistics'])

@router.get("/stat")
async def show_stat():
    return {"": ""}

@router.post("/add")
async def add_stat(task_in: TaskIn, 
                   task_dao: TaskDao = Depends(get_task_dao),
                   stat_dao: StatisticsDao = Depends(get_stat_dao)
):
    task_obj = await create_task(task_in, task_dao)
    uuid_, search_phrase = await add_task_to_scheduler(dao=stat_dao, task_obj=task_obj)
    return {
        "id": uuid_,
        "search_phrase": search_phrase
        }

@router.post("/remove")
async def remove_stat():
    return {"": ""}