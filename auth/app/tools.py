from contextlib import asynccontextmanager

from app.framework.database import AsyncSession


@asynccontextmanager
async def transaction(session: AsyncSession):
    try:
        yield session
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise e
