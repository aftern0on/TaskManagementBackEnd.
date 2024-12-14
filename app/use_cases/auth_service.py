from secrets import compare_digest

from jwt import InvalidTokenError

from app.entities.user import UserEntity
from app.interface.repository import IUserRepository, ITokenRepository
from app.use_cases.security import create_token


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
    def __init__(self, user_repo: IUserRepository, token_repo: ITokenRepository):
        self.user_repo = user_repo
        self.token_repo = token_repo

    async def execute(self, username: str, password: str) -> dict:
        user = await self.user_repo.get_by_username(username)
        if not user or not user.verify_password(password):
            raise ValueError("Неверный логин или пароль")
        access, access_expire = create_token("access", user.id)
        refresh, refresh_expire = create_token("refresh")
        print(f"id: {user.id}")
        await self.token_repo.save(user.id, refresh, refresh_expire)
        tokens = {
            "access": access,
            "refresh": refresh,
        }
        return tokens


class RefreshUseCase:
    def __init__(self, token_repo: ITokenRepository):
        self.token_repo: ITokenRepository = token_repo

    async def execute(self, refresh_token: str) -> dict:
        if await self.token_repo.get_user(refresh_token):
            user = await self.token_repo.get_user(refresh_token)
            await self.token_repo.delete(refresh_token)
            access, access_expire = create_token("access", user.id)
            refresh, refresh_expire = create_token("refresh")
            tokens = {
                "access": access,
                "refresh": refresh,
            }
            return tokens
        raise InvalidTokenError("Несуществующий refresh токен")
