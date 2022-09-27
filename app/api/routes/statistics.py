import uuid
from fastapi import APIRouter, Depends, Response
from fastapi.exceptions import HTTPException
from apscheduler.jobstores.base import JobLookupError

from ...db.dao import TaskDao, StatisticsDao
from ...db.models.task import TaskStatus
from ...schemas.task import ShowTaskStatisticsIn, ShowTaskStatisticOut, TaskIn, TaskAddOut
from ..dependencies.task import get_task_dao
from ..dependencies.statistics import get_stat_dao
from ...services.scheduler import add_task_to_scheduler, remove_task
from ...services.task import create_task, get_task_by_id, check_task_status, enable_task
from ...services.statistics import get_stat_filtered_by_date


router = APIRouter(prefix='', tags=['statistics'])

@router.post("/stat", response_model=ShowTaskStatisticOut)
async def show_stat(
    data_in: ShowTaskStatisticsIn,
    task_dao: TaskDao = Depends(get_task_dao),
    stat_dao: StatisticsDao = Depends(get_stat_dao)
    ):
    
    task = await get_task_by_id(id=data_in.id, task_dao=task_dao)
    stats = await get_stat_filtered_by_date(stat_dao=stat_dao, date_start=data_in.start, date_end=data_in.end, task_id=task.id)
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

@router.post("/stop/{id}")
async def stop_stat(
    id: uuid.UUID,
    task_dao: TaskDao = Depends(get_task_dao)
):
    task = await get_task_by_id(id, task_dao)
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task with this id not found"
        )
    task_status_check = await check_task_status(task, TaskStatus.STOPPED)
    if not task_status_check:
        raise HTTPException(
            status_code=400,
            detail=f"Task status alredy {task.status.name.lower()}"
        )
        
    await remove_task(task, task_dao)

    return Response(status_code=200)

@router.post("/start/{id}")
async def start_stat(
    id: uuid.UUID,
    task_dao: TaskDao = Depends(get_task_dao),
    stat_dao: StatisticsDao = Depends(get_stat_dao)
):
    task = await get_task_by_id(id, task_dao)
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task with this id not found"
        )
    task_status_check = await check_task_status(task, TaskStatus.RUNNING)
    if not task_status_check:
        raise HTTPException(
            status_code=400,
            detail=f"Task status alredy {task.status.name.lower()}"
        )
        
    await enable_task(task, task_dao)
    await add_task_to_scheduler(task, stat_dao)

    return Response(status_code=200)