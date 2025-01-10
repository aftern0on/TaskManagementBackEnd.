import os
import aiohttp


async def register_new_project(user_id: int) -> bool:
    """Регистрация нового пользовательского проекта по умолчанию после регистрации."""
    x_api_key = os.getenv("X_API_KEY")
    if not x_api_key:
        raise ValueError(f"Empty x_api_key in .env or .env file loading error")
    async with aiohttp.ClientSession() as session:
        headers = {"X-API-KEY": x_api_key}
        body = {
            "name": "Default",
            "creator_id": user_id
        }
        async with session.post("http://127.0.0.1:8001/i/project", headers=headers, json=body) as response:
            body = await response.json()
            project_id = body.get("id")
            print(f"Create new project ID={project_id} for user ID={user_id}")
            return project_id
