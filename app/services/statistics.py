import uuid
from ..db.dao import StatisticsDao
from ..db.models import Statistics
from ..schemas.statistics import StatisticsInDB

async def create_statistics(create_scheme: StatisticsInDB, stat_dao: StatisticsDao) -> Statistics:
    create_scheme.id = uuid.uuid4()
    stat_obj = await stat_dao.save(create_scheme)
    await stat_dao.commit()
    return stat_obj


async def get_all_statistics(stat_dao: StatisticsDao) -> list[Statistics]:
    stat_objects = await stat_dao.get_many()
    return stat_objects