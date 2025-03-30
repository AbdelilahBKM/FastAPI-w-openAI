from fastapi import HTTPException
import httpx
from typing import List
from app.utils.functions import generate_user
from app.CRUD.user_crud import add_user_to_db
from dotenv import load_dotenv
import os
load_dotenv()
DOT_NET_API = os.getenv("ASPNET_API_URL")

async def get_users_asp() -> List[dict]:
    async with httpx.AsyncClient as client:
        response = await client.get(f"{DOT_NET_API}/UserIdentity")
        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=response.status_code, detail=response.text)


async def generate_new_users(nbr_users: int, db) -> List[dict]:
    list_users = generate_user(nbr_users)
    for user in list_users:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{DOT_NET_API}/UserIdentity", json=user)
            if response.status_code == 200:
                user["token"] = response.json().get("token")
                await add_user_to_db(user, db)
            else:
                raise HTTPException(status_code=response.status_code, detail=response.text)
    return list_users