from fastapi import APIRouter, Depends

from app.db.models import Project
from app.dependencies import get_project_repo, get_auth_user_from_bearer, auth_from_api_key
from app.repositories.projects import ProjectRepository
from app.schemas.auth import UserBase
from app.schemas.project import CreateProject, ResultGetProject, ResultCreateProject, PatchProject, ResultPatchProject, \
    ICreateProject
from app.services.permission_service import PermissionService

router = APIRouter(prefix='/project', tags=["project"])
internal_router = APIRouter(prefix="/i/project", tags=["_project"])
# TODO: Добавить ограничение на internal_router для внешних IP


@router.get("/{project_id}", response_model=ResultGetProject)
async def get_project(
        project_id: int,
        project_repo: ProjectRepository = Depends(get_project_repo),
        user: UserBase = Depends(get_auth_user_from_bearer)
):
    """Получение проекта по его идентификатору"""
    project: Project = await project_repo.get_by_id(project_id, ["tasks"])
    await PermissionService.is_member(project, user.id, raise_error=True)
    return ResultGetProject.from_orm(project)


@router.patch("/{project_id}", response_model=ResultPatchProject)
async def patch_project(
        project_id: int, proj_patch: PatchProject,
        project_repo: ProjectRepository = Depends(get_project_repo),
        user: UserBase = Depends(get_auth_user_from_bearer)
):
    """Обновление существующего Project. Необязательно отправлять все поля, достаточно только обновленные"""
    project: Project = await project_repo.get_by_id(project_id)
    await PermissionService.is_creator(project, user.id, raise_error=True)
    updated_project: Project = await project_repo.update(project_id, proj_patch.dict())
    return ResultPatchProject.from_orm(updated_project)


@router.post("/", response_model=ResultCreateProject)
async def create_project(
        proj_create: CreateProject,
        project_repo: ProjectRepository = Depends(get_project_repo),
        user: UserBase = Depends(get_auth_user_from_bearer)
):
    """Создание нового проекта, который будет содержать задачи"""
    new_project: Project = Project(**proj_create.dict(), creator_id=user.id)
    project: Project = await project_repo.create(new_project)
    return ResultCreateProject.from_orm(project)


@router.delete("/{project_id}")
async def delete_project(
        project_id: int,
        project_repo: ProjectRepository = Depends(get_project_repo),
        user: UserBase = Depends(get_auth_user_from_bearer)
):
    """Удалить проект с указанным идентификатором"""
    project: Project = await project_repo.get_by_id(project_id, ["tasks"])
    await PermissionService.is_creator(project, user.id, raise_error=True)
    await project_repo.delete(project)
    return project_id


@internal_router.post("/", response_model=ResultCreateProject)
async def _create_project(
        proj_create: ICreateProject,
        project_repo: ProjectRepository = Depends(get_project_repo),
        x_api_auth: str = Depends(auth_from_api_key)
):
    """Внутренний метод создания проекта пользователя, доступен только по специальному заголовку"""
    new_project: Project = Project(**proj_create.dict())
    project: Project = await project_repo.create(new_project)
    return ResultCreateProject.from_orm(project)
