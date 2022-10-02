import pytest
from app.services.task import *
from app.schemas.task import TaskIn
from app.db.models.task import TaskStatus, Task
from app.db.dao import TaskDao

@pytest.mark.asyncio
async def test_create_task(task_dao: TaskDao):
    task_obj = await create_task(
        in_scheme=TaskIn(search_phrase="test"), 
        task_dao=task_dao
    )
    task = await task_dao.get(id=task_obj.id)
    
    assert task_obj == task
    
@pytest.mark.asyncio
async def test_get_all_tasks(task_dao: TaskDao, test_tasks: list[Task]):
    tasks = await get_all_tasks(task_dao)
    
    assert test_tasks==tasks
    
@pytest.mark.asyncio
async def test_get_task_by_id(task_dao: TaskDao, test_tasks: list[Task]):
    compare_task = test_tasks[0]
    task = await get_task_by_id(task_dao=task_dao, id=compare_task.id)
    
    assert task == compare_task

@pytest.mark.asyncio
async def test_get_task_by_search_phrase(task_dao: TaskDao, test_tasks: list[Task]):
    compare_task = test_tasks[0]
    task = await get_task_by_search_phrase(task_dao=task_dao, search_phrase=compare_task.search_phrase)
    
    assert task == compare_task

@pytest.mark.asyncio
async def test_disable_task(task_dao: TaskDao, test_tasks: list[Task]):
    compare_task = test_tasks[1]
    old_status = compare_task.status
    toggled_task = await disable_task(compare_task, task_dao)
    new_status = toggled_task.status
    
    assert old_status != new_status

@pytest.mark.asyncio
async def test_enable_task(task_dao: TaskDao, test_tasks: list[Task]):
    compare_task = test_tasks[0]
    old_status = compare_task.status
    toggled_task = await enable_task(compare_task, task_dao)
    new_status = toggled_task.status
    
    assert old_status != new_status

@pytest.mark.asyncio
async def test_check_task_status(test_tasks: list[Task]):
    task = test_tasks[0]
    
    assert await check_task_status(task, TaskStatus.RUNNING) == True
    assert await check_task_status(task, TaskStatus.STOPPED) == False