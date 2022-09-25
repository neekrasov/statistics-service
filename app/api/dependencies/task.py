from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ...db.dao.task import TaskDao
from ...db.base import get_session

async def get_task_dao(session: AsyncSession = Depends(get_session)) -> TaskDao:
    return TaskDao(session)