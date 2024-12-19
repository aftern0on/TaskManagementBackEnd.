from passlib.context import CryptContext

from app.entities.token import AccessTokenEntity
from app.interface.schemas import OutputUserData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserEntity:
    def __init__(self, user_id: int, username: str, hashed_password: str):
        self.id: int = int(user_id)
        self.username = username
        self.hashed_password = hashed_password
        self.access_token: AccessTokenEntity | None = None

    def verify_password(self, password: str) -> bool:
        """Проверка пароля"""
        return pwd_context.verify(password, self.hashed_password)

    @staticmethod
    def hash_password(password: str) -> str:
        """Хеширование пароля"""
        return pwd_context.hash(password)

    def get_user_data(self) -> OutputUserData:
        """Получение данных пользователя"""
        data = OutputUserData(id=self.id, username=self.username)
        return data
