from sqlalchemy.ext.asyncio import AsyncSession
from .base import BaseDAO
from ..models.task import Task


class TaskDao(BaseDAO):
    def __init__(self, session: AsyncSession):
        super().__init__(Task, session)
