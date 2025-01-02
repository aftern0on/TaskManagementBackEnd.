from fastapi import Depends

from app.db.database import AsyncSession
from app.repositories.projects import ProjectRepository
from app.repositories.tasks import TaskRepository


async def get_db() -> AsyncSession:
    async with AsyncSession() as session:
        yield session


async def get_task_repo(db: AsyncSession = Depends(get_db)) -> TaskRepository:
    return TaskRepository(db)


async def get_project_repo(db: AsyncSession = Depends(get_db)) -> ProjectRepository:
    return ProjectRepository(db)
