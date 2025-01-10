import os
from typing import Optional

from fastapi import Depends, Security, Header, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN, HTTP_401_UNAUTHORIZED

from app.db.database import AsyncSession
from app.exceptions import InternalServerError
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


async def get_auth_user_from_bearer(
        bearer: HTTPAuthorizationCredentials = Security(HTTPBearer()),
) -> UserBase:
    user: UserBase = await auth_user(bearer.credentials)
    return user


async def auth_from_api_key(
        x_api_key: HTTPAuthorizationCredentials = Security(APIKeyHeader(name='X-API-KEY'))
) -> True:
    required_key = os.getenv("X_API_KEY")
    if not required_key:
        raise InternalServerError()
    if required_key != x_api_key:
        raise HTTPException(HTTP_401_UNAUTHORIZED, "Unknown X-API-KEY")
    return x_api_key
