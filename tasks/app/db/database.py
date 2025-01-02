import os

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlmodel.ext.asyncio.session import AsyncSession

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost:5432/tasks")
engine = create_async_engine(DATABASE_URL, future=True)
AsyncSession = sessionmaker(class_=AsyncSession, autocommit=False, autoflush=False, bind=engine)


async def get_db() -> AsyncSession:
    async with AsyncSession() as session:
        yield session
