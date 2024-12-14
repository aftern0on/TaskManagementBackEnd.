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


class User(BaseUser):
    """Представление модели в базе данных"""
    id: int
    hashed_password: str

    class Config:
        from_attributes = True


class RefreshToken(BaseModel):
    """Схема запроса обновления токенов"""
    token: str
