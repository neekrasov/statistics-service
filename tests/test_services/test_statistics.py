from datetime import datetime, timedelta
from uuid import uuid4
import pytest
from app.services.statistics import *
from app.db.models import Task
from app.schemas.statistics import StatisticsInDB
from app.db.dao import StatisticsDao

@pytest.mark.asyncio
async def test_create_statistics(test_tasks: list[Task], stat_dao: StatisticsDao):
    new_stat = await create_statistics(
        StatisticsInDB(
            id=uuid4(),
            records_count=1,
            task_id=test_tasks[0].id,
            created_at=datetime.utcnow()
        ),
        stat_dao
    )
    
    check_stat = await stat_dao.get(id = new_stat.id)
    
    assert new_stat == check_stat

@pytest.mark.asyncio
async def test_get_stat_filtered_by_date(stat_dao: StatisticsDao, test_stats: list[Statistics]):
    stats = await get_stat_filtered_by_date(
        stat_dao=stat_dao,
        date_start=datetime.utcnow() - timedelta(hours=1),
        date_end=datetime.utcnow() + timedelta(hours=1),
        task_id=test_stats[0].task_id
    )
    
    assert test_stats == stats