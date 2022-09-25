import uuid

from sqlalchemy import Column, ForeignKey, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


from .base import Base

class Statistics(Base):
    __tablename__ = 'statistics'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    records_count = Column(Integer, nullable=False)
    task_id = Column(UUID(as_uuid=True), ForeignKey("task.id", ondelete='CASCADE'), nullable=False)
    task = relationship("Task", back_populates='statistics', lazy='selectin')
    created_at = Column(DateTime, nullable=False)
    
    def __repr__(self) -> str:
        return f"Statistics.\n \
                id: {self.id} \n \
                task_id: {self.task_id} \n \
                records_count: {self.records_count}"