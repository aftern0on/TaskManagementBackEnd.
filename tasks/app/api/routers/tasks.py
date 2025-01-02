from fastapi import APIRouter, Depends

from app.db.models import Task
from app.dependencies import get_task_repo
from app.repositories.tasks import TaskRepository
from app.schemas.task import GetTask, CreateTask

router = APIRouter(prefix='/task', tags=["task"])


@router.get("/", response_model=GetTask)
async def get_task(task_repo: TaskRepository = Depends(get_task_repo)):
    return None


@router.post("/", response_model=GetTask)
async def create_task(task_create: CreateTask, task_repo: TaskRepository = Depends(get_task_repo)):
    task_in: Task = Task(**task_create.dict(), creator_id=1)
    task: Task = await task_repo.create(task_in)
    task.project = 1
    return GetTask.from_orm(task)
