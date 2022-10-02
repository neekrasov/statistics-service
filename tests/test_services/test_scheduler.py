import pytest
from app.db.dao.statistics import StatisticsDao
from app.db.models.task import Task

from app.services.scheduler import _create_search_task, add_task_to_scheduler


@pytest.mark.asyncio
async def test_create_search_task(test_tasks: list[Task], stat_dao: StatisticsDao):
    stat_obj = await _create_search_task(task_obj=test_tasks[0], stat_dao=stat_dao)
    
    assert stat_obj
    
@pytest.mark.asyncio
async def test_add_task_to_scheduler(test_tasks: list[Task], stat_dao: StatisticsDao):
    uuid_, search_phrase = await add_task_to_scheduler(test_tasks[1], stat_dao)
    
    assert uuid_ == test_tasks[1].id
    assert search_phrase == test_tasks[1].search_phrase