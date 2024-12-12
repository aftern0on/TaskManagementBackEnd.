from fastapi import Depends

from app.framework.database import AsyncSession
from app.framework.repository import UserRepository
from app.interface.repository import IUserRepository


async def get_db() -> AsyncSession:
    async with AsyncSession() as session:
        yield session


async def get_user_repo(db: AsyncSession = Depends(get_db)) -> IUserRepository:
    return UserRepository(db)
