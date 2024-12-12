from abc import ABC, abstractmethod

from ..entities.user import UserEntity
from ..framework.models import User as UserModel


class IUserRepository(ABC):
    @abstractmethod
    async def get_by_username(self, username: str) -> UserEntity | None:
        pass

    @abstractmethod
    async def create(self, username: str, hashed_password: str) -> UserEntity:
        pass
