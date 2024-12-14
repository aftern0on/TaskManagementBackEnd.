import datetime

from redis.asyncio import Redis
from sqlalchemy import select

from app.entities.user import UserEntity
from app.framework.database import AsyncSession
from app.interface.repository import IUserRepository, ITokenRepository

from app.framework.models import User as UserModel


class UserRepository(IUserRepository):
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def get_by_username(self, username: str) -> UserEntity | None:
        query = select(UserModel).where(username == UserModel.username)
        result = await self.db.execute(query)
        user_db: UserModel = result.scalars().first()
        if not user_db:
            return None
        return UserEntity(
            id=user_db.id,
            username=user_db.username,
            hashed_password=user_db.hashed_password
        )

    async def get_by_id(self, user_id: int):
        print(user_id)
        query = select(UserModel).where(UserModel.id == user_id)
        result = await self.db.execute(query)
        user_db: UserModel = result.scalars().first()
        return UserEntity(
            id=user_db.id,
            username=user_db.username,
            hashed_password=user_db.hashed_password
        ) if user_db else None

    async def create(self, username: str, hashed_password: str) -> UserEntity:
        new_user = UserModel(username=username, hashed_password=hashed_password)
        self.db.add(new_user)
        print(self.db)
        await self.db.commit()
        await self.db.refresh(new_user)
        return UserEntity(
            id=new_user.id,
            username=new_user.username,
            hashed_password=new_user.hashed_password
        )


class RefreshTokenRepository(ITokenRepository):
    def __init__(self, redis_client: Redis, user_repo: IUserRepository):
        self.redis_client: Redis = redis_client
        self.user_repo: IUserRepository = user_repo

    async def get_user(self, token: str) -> UserEntity | None:
        user_id: int = await self.redis_client.get(f"refresh:{token}")
        return await self.user_repo.get_by_id(user_id)

    async def save(self, user_id: int, token: str, expire_at: int):
        ttl = int(expire_at - datetime.datetime.utcnow().timestamp())
        await self.redis_client.setex(f"refresh:{token}", ttl, user_id)

    async def delete(self, token: str):
        print(self.redis_client)
        await self.redis_client.delete(f"refresh:{token}")

