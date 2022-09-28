from uuid import UUID
from pydantic import BaseModel, validator
from datetime import datetime
from ..db.models.task import TaskStatus
from .statistics import StatisticsInDB, StatisticsOut


class TaskIn(BaseModel):
    search_phrase: str
    
    class Config:
        orm_mode=True

class TaskInDB(TaskIn):
    id: UUID
    status: TaskStatus | None = None
    created_at: datetime

class TaskOut(TaskInDB):
    statistics: list[StatisticsInDB]
    

class ShowTaskStatisticsIn(BaseModel):
    id: UUID
    start: datetime | None = None
    end: datetime | None = None
    
    @validator('start', 'end')
    def validate_date_contain_z(cls, v):
        return v.replace(tzinfo=None)
    
class ShowTaskStatisticOut(TaskIn):
    id: UUID
    statistics: list[StatisticsOut]

class TaskAddOut(TaskIn):
    id: UUID