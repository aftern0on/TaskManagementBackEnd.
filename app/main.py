from fastapi import FastAPI

from app.framework.database import init_db
from app.interface.auth import router as auth_router


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await init_db()


@app.get("/")
async def echo():
    return {"echo": True}


app.include_router(auth_router, prefix="/auth", tags=["auth"])
