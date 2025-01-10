from typing import Generic, TypeVar, Type, Any

from sqlalchemy.orm import selectinload
from sqlmodel import SQLModel, select

from app.db.database import AsyncSession
from app.exceptions import NotFoundError

T = TypeVar("T", bound=SQLModel)


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], session: AsyncSession):
        self.model = model
        self.session: AsyncSession = session

    async def create(self, obj: T) -> T:
        """Создание нового объекта в БД"""
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get_by_id(
            self, obj_id: int,
            related_fields: list[str] | None = None,
            not_found_error: bool = True
    ) -> T | None:
        """Получение объекта из БД по его ID
        :param not_found_error: выкидывать ошибку если объект не будет найден
        :param obj_id: Идентификатор объекта
        :param related_fields: Можно указать поля, которые будут подгружать связные объекты
        """
        query = select(self.model).where(self.model.id == obj_id)
        if related_fields:
            for field in related_fields:
                query = query.options(selectinload(getattr(self.model, field)))
        result = await self.session.execute(query)
        result = result.scalars().first()
        if not_found_error and result is None:
            raise NotFoundError(f"{self.model.__name__} with ID={obj_id} not found")
        return result

    async def update(self, obj_id: int, updates: dict[str, Any]) -> T | None:
        """Изменение полей объекта в БД"""
        obj = await self.get_by_id(obj_id)
        if not obj:
            return None

        for key, value in updates.items():
            if value is None: continue
            if hasattr(obj, key):
                setattr(obj, key, value)

        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj: T) -> None:
        """Удаление объекта из базы данных"""
        await self.session.delete(obj)
        await self.session.commit()
