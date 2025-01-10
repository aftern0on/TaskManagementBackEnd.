import asyncio

import aiohttp


async def register_new_project() -> bool:
    """Регистрация нового пользовательского проекта по умолчанию после регистрации."""
    async with aiohttp.ClientSession() as session:
        headers = {
            "X-API-KEY"
        }
        async with session.post("127.0.0.1:8001/project")
