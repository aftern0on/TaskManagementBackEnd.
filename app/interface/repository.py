import datetime
from abc import ABC, abstractmethod
from app.entities.user import UserEntity


class IUserRepository(ABC):
    @abstractmethod
    async def get_by_username(self, username: str) -> UserEntity | None:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int):
        pass

    @abstractmethod
    async def create(self, username: str, hashed_password: str) -> UserEntity:
        pass


class ITokenRepository(ABC):
    @abstractmethod
    async def save(self, user_id: int, token: str, expire_at: datetime):
        """Сохранение токена в redis"""
        pass

    @abstractmethod
    async def delete(self, token: str):
        """Удаление токена из redis"""
        pass

    @abstractmethod
    async def get_user(self, token: str) -> UserEntity | None:
        """Получение пользователя по его token (пока работает только с refresh)"""
        pass
