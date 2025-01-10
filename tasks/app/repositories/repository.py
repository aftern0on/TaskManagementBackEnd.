from typing import Generic, TypeVar, Type, Any, Optional

from sqlalchemy import update
from sqlalchemy.orm import selectinload
from sqlmodel import SQLModel, select, and_

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

    async def get_list(
            self,
            filters: dict[str, Any] | None,
            limit: int = 10,
            offset: int = 0,
            order_by: str | None = None,
            related_fields: list[str] | None = None
    ) -> list[T]:
        """Получение выборки объектов с фильтрацией, пагинацией, сортировкой и загрузкой связных полей
        :param filters: Словарь для фильтрации (например, {"user_id": 1})
        :param limit: Лимит на количество объектов
        :param offset: Смещение для пагинации
        :param order_by: Поле, по которому будет сортироваться объект (например, "id" или "-id")
        :param related_fields: Можно указать поля, которые будут подгружать связные объекты
        """
        query = select(self.model)
        query = query.offset(offset).limit(limit)
        if filters:
            filter_conditions = [getattr(self.model, key) == value for key, value in filters.items()]
            query = query.where(and_(*filter_conditions))
        if related_fields:
            for field in related_fields:
                query = query.options(selectinload(getattr(self.model, field)))
        if order_by:
            if order_by.startswith("-"):
                order_field = getattr(self.model, order_by[1:])
                query = query.order_by(order_field.desc())
            else:
                order_field = getattr(self.model, order_by)
                query = query.order_by(order_field)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(
            self, obj_id: int,
            related_fields: list[str] | None = None,
            not_found_error: bool = True
    ) -> T | None:
        """Получение объекта из БД по его ID
        :param not_found_error: Выкидывать ошибку если объект не будет найден
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

    async def update(self, obj_id: int, updates: dict[str, Any]) -> T:
        """Изменение полей объекта в БД"""
        query = (
            update(self.model)
            .where(self.model.id == obj_id)
            .values(**updates)
            .returning(self.model)
        )
        result = await self.session.execute(query)
        updated_obj = result.scalars().first()
        if not updated_obj:
            raise NotFoundError(f"{self.model.__name__} with ID={obj_id} not found")
        await self.session.commit()
        return updated_obj

    async def delete(self, obj: T) -> None:
        """Удаление объекта из базы данных"""
        await self.session.delete(obj)
        await self.session.commit()
