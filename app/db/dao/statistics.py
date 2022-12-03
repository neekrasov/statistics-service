from sqlalchemy.ext.asyncio import AsyncSession
from .base import BaseDAO
from ..models.statistics import Statistics


class StatisticsDao(BaseDAO):
    def __init__(self, session: AsyncSession):
        super().__init__(Statistics, session)
