from datetime import datetime
from typing import List

from sqlmodel import Field, Relationship, ARRAY, Column, Integer
from app.schemas.project import ProjectBase
from app.schemas.task import TaskBase


class Task(TaskBase, table=True):
    __tablename__ = "tasks"
    id: int = Field(default=None, primary_key=True, index=True)
    name: str
    description: str | None
    status: str = Field(default="start")
    priority: str = Field(default="normal")
    deadline: datetime | None
    create_time: datetime = Field(default_factory=datetime.utcnow)
    last_update_time: datetime = Field(default_factory=datetime.utcnow)
    creator_id: int
    executor_id: int | None = None
    project_id: int = Field(foreign_key="projects.id")
    project: 'Project' = Relationship(back_populates='tasks')


class Project(ProjectBase, table=True):
    __tablename__ = "projects"
    id: int = Field(default=None, primary_key=True, index=True)
    name: str
    description: str = ""
    creator_id: int
    users_ids: List[int] = Field(default=[], sa_column=Column(ARRAY(Integer)))
    tasks: list[Task] | None = Relationship(back_populates='project')
