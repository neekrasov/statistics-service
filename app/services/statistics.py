import uuid
from ..db.dao import StatisticsDao
from ..db.models import Statistics
from ..schemas.statistics import StatisticsInDB

async def create_statistics(create_scheme: StatisticsInDB, stat_dao: StatisticsDao) -> Statistics:
    create_scheme.id = uuid.uuid4()
    stat_obj = await stat_dao.save(create_scheme)
    await stat_dao.commit()
    return stat_obj

async def get_stat_filtered_by_date(stat_dao: StatisticsDao, date_start, date_end, task_id: uuid.UUID) -> list[Statistics]:
    stat_objects = await stat_dao.get_many(Statistics.created_at >= date_start, Statistics.created_at <= date_end, task_id=task_id)
    return stat_objects
    