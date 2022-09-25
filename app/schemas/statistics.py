from uuid import UUID
from pydantic import BaseModel
from datetime import datetime


class StatisticsIn(BaseModel):
    records_count: int
    
    class Config:
        orm_mode=True

class StatisticsInDB(StatisticsIn):
    id: UUID | None = None
    task_id: UUID
    created_at: datetime

class StatisticsOut(StatisticsInDB):
    pass