import pytest
from uuid import uuid4
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from app.schemas.task import ShowTaskStatisticsIn, TaskInDB
from app.api.dependencies.task import get_task_dao
from app.db.models.task import TaskStatus


@pytest.mark.asyncio
async def test_add_stat(client: AsyncClient):
    result = await client.post("/api/v1/add", json={"search_phrase": 'testing'})
    
    assert result.status_code == 200
    
@pytest.mark.asyncio
async def test_repeated_add_stat(client: AsyncClient):
    await client.post("/api/v1/add", json={"search_phrase": 'testing'})
    result = await client.post("/api/v1/add", json={"search_phrase": 'testing'})
    
    assert result.status_code == 400
    assert result.json()["detail"]
    assert result.json()["task_id"]
    
@pytest.mark.asyncio
async def test_show_stat(client: AsyncClient):
    response = await client.post("/api/v1/add", json={"search_phrase": 'testing'})
    task_id = response.json()["id"]
    post_data = ShowTaskStatisticsIn(
        id=task_id,
        start=datetime.utcnow() - timedelta(minutes=10),
        end=datetime.utcnow() + timedelta(minutes=10)
    )
    result = await client.post("/api/v1/stat", content=post_data.json())
    
    assert result.status_code == 200

@pytest.mark.asyncio
async def test_show_stat_invalid_uuid(client: AsyncClient):
    post_data = ShowTaskStatisticsIn(
        id=uuid4(),
        start=datetime.utcnow() - timedelta(minutes=10),
        end=datetime.utcnow() + timedelta(minutes=10)
    )
    result = await client.post("/api/v1/stat", content=post_data.json())
    
    assert result.status_code == 404

@pytest.mark.asyncio
async def test_stop_stat(client: AsyncClient):
    response = await client.post("/api/v1/add", json={"search_phrase": 'testing'})
    task_id = response.json()["id"]
    result = await client.post(f"/api/v1/stop/{task_id}")
    
    assert result.status_code == 200

@pytest.mark.asyncio
async def test_stop_stat_invalid_uuid(client: AsyncClient):
    result = await client.post(f"/api/v1/stop/{uuid4()}")
    
    assert result.status_code == 404

@pytest.mark.asyncio
async def test_stop_stat_already_stopped(client: AsyncClient, session: AsyncSession):
    
    task_dao = await get_task_dao(session=session)
    task_obj = await task_dao.save(TaskInDB(
        id = uuid4(),
        search_phrase="test",
        created_at = datetime.utcnow(),
        status=TaskStatus.STOPPED.name
    ))
    await task_dao.commit()
    result = await client.post(f"/api/v1/stop/{task_obj.id}")
    
    assert result.status_code == 400
    
@pytest.mark.asyncio
async def test_start_stat(client: AsyncClient, session: AsyncSession):
    task_dao = await get_task_dao(session=session)
    task_obj = await task_dao.save(TaskInDB(
        id = uuid4(),
        search_phrase="test",
        created_at = datetime.utcnow(),
        status=TaskStatus.STOPPED.name
    ))
    await task_dao.commit()
    result = await client.post(f"/api/v1/start/{task_obj.id}")
    
    assert result.status_code == 200

@pytest.mark.asyncio
async def test_start_stat_invalid_uuid(client: AsyncClient):
    result = await client.post(f"/api/v1/start/{uuid4()}")
    
    assert result.status_code == 404

@pytest.mark.asyncio
async def test_start_stat_already_running(client: AsyncClient):
    response = await client.post("/api/v1/add", json={"search_phrase": 'testing'})
    task_id = response.json()["id"]

    result = await client.post(f"/api/v1/start/{task_id}")
    
    assert result.status_code == 400
