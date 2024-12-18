import os

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import AsyncSession as _AsyncSession

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost:5432/db")
engine = create_async_engine(DATABASE_URL, future=True)
AsyncSession = sessionmaker(class_=_AsyncSession, autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
