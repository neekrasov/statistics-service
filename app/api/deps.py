from typing import Callable, Type
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.dao.base import BaseDAO
from ..db.base import SessionLocal

async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

def get_dao(
    repo_type: Type[BaseDAO],
) -> Callable[[AsyncSession], BaseDAO]:
    
    def _get_dao(
        session: AsyncSession = Depends(get_session),
    ) -> BaseDAO:
        return repo_type(session)

    return _get_dao