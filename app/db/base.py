from typing import AsyncGenerator, Callable
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker


def create_session_factory(uri: str | None) -> sessionmaker:
    engine: AsyncEngine = create_async_engine(uri, echo=True)
    session_factory = sessionmaker(
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession
    )
    return session_factory


def async_session(
    uri: str | None
) -> Callable[..., AsyncGenerator[AsyncSession, None]]:

    if not uri:
        raise ValueError("No database URI provided")

    session_factory = create_session_factory(uri)

    async def get_session() -> AsyncGenerator[AsyncSession, None]:
        async with session_factory() as session:
            yield session

    return get_session
