from pydantic import BaseModel


class BaseUser(BaseModel):
    """Базовая модель пользователя"""
    username: str


class LoginUser(BaseUser):
    """Схема для авторизации пользователя"""
    password: str


class RegisterUser(LoginUser):
    """Схема регистрации пользователя"""
    confirm_password: str


class OutputUserData(BaseUser):
    """Форма данных пользователя"""
    id: int


class RefreshToken(BaseModel):
    """Схема запроса обновления токенов"""
    refresh: str
