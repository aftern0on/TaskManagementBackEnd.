from fastapi import Depends

from app.framework.database import AsyncSession
from app.framework.redis import redis_client
from app.framework.repository import UserRepository, RefreshTokenRepository
from app.interface.repository import IUserRepository, ITokenRepository


async def get_db() -> AsyncSession:
    async with AsyncSession() as session:
        yield session


async def get_user_repo(db: AsyncSession = Depends(get_db)) -> IUserRepository:
    return UserRepository(db)


async def get_refresh_token_repo(user_repo: UserRepository = Depends(get_user_repo)) -> ITokenRepository:
    return RefreshTokenRepository(redis_client, user_repo)

