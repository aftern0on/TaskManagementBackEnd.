from fastapi import Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.db.database import AsyncSession
from app.repositories.projects import ProjectRepository
from app.repositories.tasks import TaskRepository
from app.schemas.auth import UserBase
from app.services.grpc_service import auth_user


async def get_db() -> AsyncSession:
    async with AsyncSession() as session:
        yield session


async def get_task_repo(db: AsyncSession = Depends(get_db)) -> TaskRepository:
    return TaskRepository(db)


async def get_project_repo(db: AsyncSession = Depends(get_db)) -> ProjectRepository:
    return ProjectRepository(db)


async def get_auth_user_from_credentials(
        credentials: HTTPAuthorizationCredentials = Security(HTTPBearer())
) -> UserBase:
    user: UserBase = await auth_user(credentials.credentials)
    return user
