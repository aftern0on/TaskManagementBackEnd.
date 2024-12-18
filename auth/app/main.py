from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.framework.redis import redis_client
from app.interface.auth import router as auth_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
async def echo():
    """Проверка состояния текущего сервиса авторизации."""
    return {"echo": True}


@app.get("/redis_ping")
async def redis():
    """Проверка состояния redis сервиса."""
    try:
        pong = await redis_client.ping()
        return {"redis": "alive" if pong else "dead"}
    except Exception as e:
        return {"error": str(e)}


app.include_router(auth_router, prefix="/auth", tags=["auth"])
