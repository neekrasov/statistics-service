import enum
import uuid

from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base

class TaskStatus(enum.Enum):
    RUNNING = 'RUNNING'
    STOPPED = 'STOPPED'


class Task(Base):
    __tablename__ = "task"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    search_phrase = Column(String, nullable=False)
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.RUNNING)
    created_at = Column(DateTime, nullable=False)
    statistics = relationship("Statistics", back_populates='task', lazy='selectin', cascade='all, delete-orphan')
    
    def __repr__(self) -> str:
        return f"Task.\n \
            id: {self.id} \n \
            search_phrase: {self.search_phrase} \n \
            status: {self.status} \n \
            created_at: {self.created_at}"