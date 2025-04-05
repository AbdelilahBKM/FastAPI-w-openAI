from fastapi import HTTPException
from typing import List
import httpx
import os
import random
from dotenv import load_dotenv
from app.models import User, Discussion, Joining
from app.CRUD.joining_crud import create_joining_to_db
from app.CRUD.user_crud import get_random_users
from app.CRUD.discussion_crud import get_local_discussions

load_dotenv()
DOT_NET_API = os.getenv("ASPNET_API_URL")

async def create_multiple_joining_to_discussion(discussions: Discussion, db) -> List[Joining] | None:
    users = await get_random_users(db, random.randint(7, 25))
    joinings: List[Joining] = []
    for user in users:
        async with httpx.AsyncClient() as client:
            joining = {
                "user_id": user.id,
                "discussion_id": discussions.id
            }
            response = await client.post(
                f"{DOT_NET_API}/Joining",
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {user.token}"},
                data=joining
            )
            if response.status_code == 200:
                create_joining_to_db(response.json(), db)
                joinings.append(response.json())
            else:
                raise HTTPException(status_code=response.status_code, detail=response.text)
    return joinings

async def create_joining_to_discussions(db) -> None:
    discussions = get_local_discussions(db)
    for discussion in discussions:
        joining = await create_multiple_joining_to_discussion(discussion, db)
        print(joining)

