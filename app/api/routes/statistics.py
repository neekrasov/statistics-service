import uuid

from fastapi import APIRouter, Depends, Response
from fastapi.exceptions import HTTPException

from app.core.di.stubs import (
    provide_scheduler_service_stub,
    provide_stat_service_stub,
    provide_task_service_stub
)
from app.db.models.task import TaskStatus
from app.schemas.task import (ShowTaskStatisticOut, ShowTaskStatisticsIn,
                              TaskAddOut, TaskIn)
from app.services import SchedulerService, StatisticsService, TaskService

router = APIRouter(prefix="", tags=["statistics"])


@router.post("/stat", response_model=ShowTaskStatisticOut)
async def show_stat(
    data_in: ShowTaskStatisticsIn,
    task_service: TaskService = Depends(provide_task_service_stub),
    stat_service: StatisticsService = Depends(provide_stat_service_stub),
):

    task = await task_service.get_task_by_id(id=data_in.id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task with this id not found"
        )
    stats = await stat_service.get_stat_filtered_by_date(
        date_start=data_in.start, date_end=data_in.end, task_id=task.id
    )
    task.statistics = stats
    return task


@router.post("/add", response_model=TaskAddOut)
async def add_stat(
    task_in: TaskIn,
    task_service: TaskService = Depends(provide_task_service_stub),
    stat_service: StatisticsService = Depends(provide_stat_service_stub),
    scheduler_service: SchedulerService = Depends(
        provide_scheduler_service_stub
    )
):
    task = await task_service.get_task_by_search_phrase(task_in.search_phrase)
    if task:
        raise HTTPException(
            detail={
                "message": "A task with this search query already exists.",
                "task_id": str(task.id),
            },
            status_code=400,
        )
    task_obj = await task_service.create_task(task_in)
    await scheduler_service.add_task(task_obj=task_obj)
    return task_obj


@router.post("/stop/{id}")
async def stop_stat(
    id: uuid.UUID,
    task_service: TaskService = Depends(provide_task_service_stub),
    scheduler_service: SchedulerService = Depends(
        provide_scheduler_service_stub
    )
):
    task = await task_service.get_task_by_id(id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task with this id not found"
        )

    task_status_check = await task_service.check_task_status(
        task=task,
        expected_status=TaskStatus.STOPPED
    )
    if not task_status_check:
        raise HTTPException(
            status_code=400,
            detail=f"Task status already {task.status.name.lower()}"
        )

    status = await scheduler_service.remove_task(task.id)
    if status:
        await task_service.disable_task(task)

    return Response(status_code=200)


@router.post("/start/{id}")
async def start_stat(
    id: uuid.UUID,
    task_service: TaskService = Depends(provide_task_service_stub),
    scheduler_service: SchedulerService = Depends(
        provide_scheduler_service_stub
    )
):
    task = await task_service.get_task_by_id(id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task with this id not found"
        )

    task_status_check = await task_service.check_task_status(
        task=task,
        expected_status=TaskStatus.RUNNING,
    )
    if not task_status_check:
        raise HTTPException(
            status_code=400,
            detail=f"Task status already {task.status.name.lower()}"
        )

    await task_service.enable_task(task)
    await scheduler_service.add_task(task)

    return Response(status_code=200)
