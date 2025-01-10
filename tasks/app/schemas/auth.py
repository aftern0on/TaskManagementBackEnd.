from sqlmodel import SQLModel


class UserBase(SQLModel):
    """Модель с данными авторизованного пользователя"""
    id: int
    username: str
