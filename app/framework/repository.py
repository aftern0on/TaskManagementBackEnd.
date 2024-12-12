from sqlalchemy import select

from app.entities.user import UserEntity
from app.framework.database import AsyncSession
from app.interface.repository import IUserRepository

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

    async def create(self, username: str, hashed_password: str) -> UserEntity:
        new_user = UserModel(username=username, hashed_password=hashed_password)
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return UserEntity(
            id=new_user.id,
            username=new_user.username,
            hashed_password=new_user.hashed_password
        )
