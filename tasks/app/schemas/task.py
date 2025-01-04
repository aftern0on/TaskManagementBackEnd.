from datetime import datetime

from sqlmodel import SQLModel


class TaskBase(SQLModel):
    """Параметры, которые можно задать вручную при создании объекта"""
    name: str
    description: str | None = None
    status: str | None = "open"
    priority: str | None = "medium"
    deadline: datetime | None = None
    executor_id: int | None = None


class CreateTask(TaskBase):
    """Схема создания задачи"""
    project_id: int


class UpdateTask(TaskBase):
    """Схема обновления задачи"""
    name: str | None = None
    description: str | None = None
    status: str | None = None
    priority: str | None = None
    deadline: datetime | None = None
    executor_id: int | None = None


class GetTask(TaskBase):
    """Схема задачи"""
    id: int
    creator_id: int
    create_time: datetime
    last_update_time: datetime
    project_id: int
