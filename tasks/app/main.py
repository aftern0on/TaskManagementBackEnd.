from fastapi import FastAPI
from api.routers.tasks import router as tasks_router

app = FastAPI()
app.include_router(tasks_router, prefix='/task', tags=["task"])


@app.get('/tasks_ping')
async def ping():
    return {'pong': True}
