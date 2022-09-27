from fastapi import APIRouter, Depends

from ...db.dao import TaskDao, StatisticsDao
from ...schemas.task import ShowTaskStatisticsIn, ShowTaskStatisticOut, TaskIn, TaskAddOut
from ..dependencies.task import get_task_dao
from ..dependencies.statistics import get_stat_dao
from ...services.scheduler import add_task_to_scheduler
from ...services.task import create_task, get_task_by_id
from ...services.statistics import get_stat_filtered_by_date


router = APIRouter(prefix='', tags=['statistics'])

@router.post("/stat", response_model=ShowTaskStatisticOut)
async def show_stat(
    data_in: ShowTaskStatisticsIn,
    task_dao: TaskDao = Depends(get_task_dao),
    stat_dao: StatisticsDao = Depends(get_stat_dao)
    ):
    
    task = await get_task_by_id(id=data_in.id, task_dao=task_dao)
    stats = await get_stat_filtered_by_date(stat_dao=stat_dao, date_start=data_in.start, date_end=data_in.end)
    task.statistics = stats
    return task

@router.post("/add", response_model=TaskAddOut)
async def add_stat(
    task_in: TaskIn, 
    task_dao: TaskDao = Depends(get_task_dao),
    stat_dao: StatisticsDao = Depends(get_stat_dao)
):
    task_obj = await create_task(task_in, task_dao)
    await add_task_to_scheduler(dao=stat_dao, task_obj=task_obj)
    return task_obj

@router.post("/remove")
async def remove_stat():
    return {"": ""}