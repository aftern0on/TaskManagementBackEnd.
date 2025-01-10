from typing import List

from sqlalchemy import Integer
from sqlmodel import SQLModel, Field, ARRAY, Column

from app.schemas.task import GetTask


class ProjectBase(SQLModel):
    """Параметры, которые можно задать вручную при создании объекта"""
    name: str
    description: str = ""
    users_ids: List[int] = Field(default=[], sa_column=Column(ARRAY(Integer)))


class CreateProject(ProjectBase):
    """Схема создания проекта"""
    pass


class ICreateProject(CreateProject):
    """Схема создания проекта для внутреннего API"""
    creator_id: int


class PatchProject(SQLModel):
    """Схема обновление существующего проекта"""
    name: str | None = None
    description: str | None = None


class ResultCreateProject(CreateProject):
    """Схема результата создания проекта"""
    id: int
    creator_id: int


class ResultPatchProject(ResultCreateProject):
    """Схема результата обновления проекта"""
    pass


class ResultGetProject(ProjectBase):
    """Схема проекта"""
    id: int
    creator_id: int
    tasks: List[GetTask] = []
