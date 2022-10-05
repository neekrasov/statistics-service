import asyncio
from datetime import datetime, timedelta
from uuid import uuid4
from httpx import AsyncClient
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession
from app.db.base import engine
from app.api.deps import get_session, get_dao
from app.db.models.task import TaskStatus
from app.db.models import Statistics, Task
from app.main import app
from app.db.dao import TaskDao, StatisticsDao
from app.schemas.statistics import StatisticsInDB
from app.schemas.task import TaskInDB

@pytest_asyncio.fixture(scope="session", autouse=True)
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture()
async def connection():
    async with engine.begin() as conn:
        yield conn
        await conn.rollback()

@pytest_asyncio.fixture()
async def session(connection: AsyncConnection):
    async with AsyncSession(connection, expire_on_commit=False) as _session:
        yield _session
        
@pytest_asyncio.fixture()
async def task_dao(session: AsyncSession) -> TaskDao:
    return get_dao(TaskDao)(session)

@pytest_asyncio.fixture()
async def stat_dao(session: AsyncSession) -> StatisticsDao:
    return get_dao(StatisticsDao)(session)

@pytest_asyncio.fixture(autouse=True)
async def override_dependency(session: AsyncSession):
    app.dependency_overrides[get_session] = lambda: session
    
@pytest_asyncio.fixture()
async def clear_db(task_dao: TaskDao):
    tasks = await task_dao.get_many()
    for task in tasks:
        await task_dao.delete(db_obj = task)

@pytest_asyncio.fixture()
async def test_tasks(task_dao: TaskDao, clear_db) -> list[Task]:
    task_list = [await task_dao.save(
        TaskInDB(
            id = uuid4(),
            search_phrase=search_phrase,
            created_at = datetime.utcnow(),
            status=TaskStatus.STOPPED.name if index%2==0 else TaskStatus.RUNNING.name
    )) for index, search_phrase in enumerate(['first_task', 'second_task', 'third_task'])]
    await task_dao.commit()
    return task_list

@pytest_asyncio.fixture()
async def test_stats(stat_dao: StatisticsDao, test_tasks: list[Task])-> list[Statistics]:
    stats_list = [
        await stat_dao.save(
            StatisticsInDB(
                id=uuid4(),
                records_count=1,
                task_id=test_tasks[0].id,
                created_at=datetime.utcnow() + timedelta(minutes=minutes)
        )) for minutes in range(0, 30, 10)
    ]
    await stat_dao.commit()
    return stats_list

@pytest_asyncio.fixture(scope="session")
async def client() -> AsyncClient:
    async with AsyncClient(
        app=app,
        base_url="http://test",
    ) as client:
        yield client
