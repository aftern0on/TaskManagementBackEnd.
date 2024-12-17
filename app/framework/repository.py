import datetime

from redis.asyncio import Redis
from sqlalchemy import select

from app.entities.token import RefreshTokenEntity
from app.entities.user import UserEntity
from app.framework.database import AsyncSession
from app.framework.models import User as UserModel


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def get_by_username(self, username: str) -> UserEntity | None:
        """Получить пользователя из БД по его Username"""
        query = select(UserModel).where(username == UserModel.username)
        result = await self.db.execute(query)
        user_db: UserModel = result.scalars().first()
        if not user_db:
            return None
        return UserEntity(
            user_id=user_db.id,
            username=user_db.username,
            hashed_password=user_db.hashed_password
        )

    async def get_by_id(self, user_id: int):
        """Получить пользователя из БД по его ID"""
        query = select(UserModel).where(UserModel.id == user_id)
        result = await self.db.execute(query)
        user_db: UserModel = result.scalars().first()
        return UserEntity(
            user_id=user_db.id,
            username=user_db.username,
            hashed_password=user_db.hashed_password
        ) if user_db else None

    async def create(self, username: str, hashed_password: str) -> UserEntity:
        """Создание нового пользователя в БД"""
        new_user = UserModel(username=username, hashed_password=hashed_password)
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return UserEntity(
            user_id=new_user.id,
            username=new_user.username,
            hashed_password=new_user.hashed_password
        )


class TokenRepository:
    def __init__(self, redis_client: Redis, user_repo: UserRepository):
        self.redis_client: Redis = redis_client
        self.user_repo: UserRepository = user_repo

    async def get_user_by_refresh(self, token: str) -> UserEntity | None:
        """Получение пользователя по его refresh-токену, также по совместительству проверка существования токена"""
        redis_data = await self.redis_client.get(f"refresh:{token}")
        if not redis_data: return None
        user_id: int = int(redis_data)
        return await self.user_repo.get_by_id(user_id)

    async def save_refresh(self, token: RefreshTokenEntity, ttl: int, user_id: int):
        """Сохранение refresh-токена для идентификации и последующего использования"""
        await self.redis_client.setex(f"refresh:{token.value}", ttl, user_id)

    async def drop_refresh(self, token: RefreshTokenEntity):
        """Удаление refresh-токена из хранилища и сделать его недействительным"""
        await self.redis_client.delete(f"refresh:{token}")
