from fastapi import APIRouter, Depends

from app.db.models import Task, Project
from app.dependencies import get_task_repo, get_project_repo, get_auth_user_from_credentials
from app.exceptions import ForbiddenError
from app.repositories.projects import ProjectRepository
from app.repositories.tasks import TaskRepository
from app.schemas.auth import UserBase
from app.schemas.task import GetTask, CreateTask, UpdateTask

router = APIRouter(prefix='/task', tags=["task"])


@router.get("/{task_id}", response_model=GetTask)
async def get_task(task_id: int, task_repo: TaskRepository = Depends(get_task_repo)):
    """Получение задачи по его идентификатору"""
    task: Task = await task_repo.get_by_id(task_id)
    return GetTask.from_orm(task)


@router.patch("/{task_id}", response_model=GetTask)
async def update_task(task_id: int, updates: UpdateTask, task_repo: TaskRepository = Depends(get_task_repo)):
    """Обновление существующей задачи. Необязательно отправлять все поля, достаточно только обновленные"""
    task: Task = await task_repo.update(task_id, updates.dict())
    return GetTask.from_orm(task)


@router.post("/", response_model=GetTask)
async def create_task(
        task_create: CreateTask,
        task_repo: TaskRepository = Depends(get_task_repo),
        proj_repo: ProjectRepository = Depends(get_project_repo),
        user: UserBase = Depends(get_auth_user_from_credentials)
):
    """Создание новой задачи"""
    project: Project = await proj_repo.get_by_id(task_create.project_id)
    task_in: Task = Task(**task_create.dict(), creator_id=user.id)
    task_in.project = project
    task: Task = await task_repo.create(task_in)
    return GetTask.from_orm(task)


@router.delete("/{task_id}")
async def delete_task(
        task_id: int, task_repo: TaskRepository = Depends(get_task_repo),
        user: UserBase = Depends(get_auth_user_from_credentials)
):
    """Удаление задачи с указанным идентификатором. Возвращает ID, если операция прошла успешно"""
    task: Task = await task_repo.get_by_id(task_id)
    if task.creator_id == user.id:
        raise ForbiddenError
    await task_repo.delete(task)
    return task_id
