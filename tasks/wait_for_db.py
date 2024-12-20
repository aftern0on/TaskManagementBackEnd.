import asyncio
import asyncpg
import os
import time


async def wait_for_db():
    retries = 10
    delay = 5
    database_url = os.getenv('DATABASE_URL')

    if not database_url:
        print("DATABASE_URL is not set.")
        exit(1)

    if database_url.startswith("postgresql+asyncpg://"):
        database_url = database_url.replace("postgresql+asyncpg://", "postgresql://", 1)

    for attempt in range(retries):
        try:

            conn = await asyncpg.connect(database_url)
            await conn.close()
            print('The database is available')
            return
        except (asyncpg.exceptions.CannotConnectNowError, OSError) as e:
            print(f'The next attempt to connect to the database: {attempt + 1}')
            time.sleep(delay)

    print('All attempts to connect to the database failed')
    exit(1)


if __name__ == '__main__':
    asyncio.run(wait_for_db())

