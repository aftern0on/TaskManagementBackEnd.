from fastapi import FastAPI

from app.framework.database import init_db
from app.framework.redis import redis_client
from app.interface.auth import router as auth_router


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await init_db()


@app.get("/")
async def echo():
    return {"echo": True}


@app.get("/redis_ping")
async def redis():
    try:
        pong = await redis_client.ping()
        return {"redis": "alive" if pong else "dead"}
    except Exception as e:
        return {"error": str(e)}


app.include_router(auth_router, prefix="/auth", tags=["auth"])
