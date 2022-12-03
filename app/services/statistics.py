import uuid
from ..db.dao import StatisticsDao
from ..db.models import Statistics as StatisticsModel
from ..schemas.statistics import StatisticsInDB, Statistics


class StatisticsService:
    def __init__(self, stat_dao: StatisticsDao):
        self.stat_dao = stat_dao

    async def create_statistics(
        self, create_scheme: StatisticsInDB
    ) -> Statistics:
        create_scheme.id = uuid.uuid4()
        stat_obj = await self.stat_dao.save(create_scheme)
        await self.stat_dao.commit()
        return Statistics.from_orm(stat_obj)

    async def get_stat_filtered_by_date(
        self, date_start, date_end, task_id: uuid.UUID
    ) -> list[Statistics]:
        stat_objects = await self.stat_dao.get_many(
            StatisticsModel.created_at >= date_start,
            StatisticsModel.created_at <= date_end,
            task_id=task_id,
        )
        return [Statistics.from_orm(stat_obj) for stat_obj in stat_objects]
