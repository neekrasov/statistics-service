from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, TypeVar, Type, Generic
from pydantic import BaseModel

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseDAO(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self._model = model
        self._session = session

    async def get(self, *args, **kwargs) -> ModelType | None:
        result = await self._session.execute(
            select(self._model).filter(*args).filter_by(**kwargs)
        )
        return result.scalars().first()

    async def get_many(
        self, *args, offset: int = 0, limit: int = 100, **kwargs
    ) -> list[ModelType]:

        result = await self._session.execute(
            select(self._model)
            .filter(*args)
            .filter_by(**kwargs)
            .offset(offset)
            .limit(limit)
        )
        return result.scalars().all()

    async def update(
            self,
            *,
            obj_in: UpdateSchemaType | dict[str, Any],
            db_obj: ModelType | None = None,
            **kwargs
    ) -> ModelType | None:

        db_obj = db_obj or await self.get(**kwargs)

        if db_obj is not None:
            obj_data = db_obj.__dict__

            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.dict(exclude_unset=True)
            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
            self._session.add(db_obj)

        return db_obj

    async def delete(
            self, *args, db_obj: ModelType | None = None, **kwargs
    ) -> ModelType:
        db_obj = db_obj or await self.get(self._session, *args, **kwargs)
        await self._session.delete(db_obj)
        return db_obj

    async def save(self, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self._model(**dict(obj_in))
        self._session.add(db_obj)
        return db_obj

    async def commit(self):
        await self._session.commit()

    async def flush(self, *objects):
        await self._session.flush(objects)
