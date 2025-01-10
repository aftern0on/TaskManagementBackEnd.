import dotenv
from fastapi import FastAPI
from app.api.routers.tasks import router as tasks_router
from app.api.routers.projects import internal_router as i_project_router
from app.api.routers.projects import router as project_router

dotenv.load_dotenv()

app = FastAPI()
app.include_router(tasks_router)
app.include_router(project_router)
app.include_router(i_project_router)


@app.get('/tasks_ping')
async def ping():
    return {'pong': True}
