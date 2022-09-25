from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ...db.dao.statistics import StatisticsDao
from ...db.base import get_session


async def get_stat_dao(session: AsyncSession = Depends(get_session)) -> StatisticsDao:
    return StatisticsDao(session)
