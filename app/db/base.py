from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from ..core.settings import get_settings

settings = get_settings()

engine = create_async_engine(settings.postgres_uri, echo=True)

SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)