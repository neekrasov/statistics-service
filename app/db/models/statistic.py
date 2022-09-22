from operator import index
import uuid

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID


from .base import Base

class Statistic(Base):
    __tablename__ = 'statistic'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    search_phrase = Column(String, nullable=False, index=True)
    records_count = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    
    def __repr__(self) -> str:
        return f"Phrase: {self.search_phrase} \n Records_count: {self.records_count} \n"