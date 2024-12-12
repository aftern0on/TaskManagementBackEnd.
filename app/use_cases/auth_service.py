from app.entities.user import UserEntity
from app.framework.database import AsyncSession
from app.interface.repository import IUserRepository
from app.use_cases.security import create_access_token
from secrets import compare_digest


class RegisterUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def execute(self, username: str, password: str, confirm_password) -> UserEntity:
        """Аутентификация пользователя, проверка введенных данных исходя из строчки в бд"""
        if not compare_digest(password, confirm_password):
            raise ValueError("Пароли не совпадают")
        existing_user = await self.user_repo.get_by_username(username)
        if existing_user:
            raise ValueError(f"Пользователь {username} уже зарегистрирован")
        hashed_password = UserEntity.hash_password(password)
        return await self.user_repo.create(username, hashed_password)


class LoginUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def execute(self, username: str, password: str):
        user = await self.user_repo.get_by_username(username)
        if not user or not user.verify_password(password):
            raise ValueError("Неверный логин или пароль")
        return create_access_token({"sub": user.username})
