from fastapi import HTTPException
import httpx
from typing import List
from app.CRUD.discussion_crud import create_discussion_to_db
from dotenv import load_dotenv
from app.CRUD.user_crud import get_random_user
from app.models import Discussion
import os
load_dotenv()
DOT_NET_API = os.getenv("ASPNET_API_URL")

async def create_discussion_asp(discussion: dict, db) -> dict:
    async with httpx.AsyncClient as client:
        response = await client.post(f"{DOT_NET_API}/Discussion", json=discussion)
        if response.status_code == 200:
            discussion["id"] = response.json().get("id")
            create_discussion_to_db(discussion, db)
            return discussion
        raise HTTPException(status_code=response.status_code, detail=response.text)

async def create_discussions_asp(discussions: List[Discussion], db) -> List[Discussion]:
    list_discussions = []
    for discussion in discussions:
        async with httpx.AsyncClient() as client:
            random_user = await get_random_user(db)
            discussion.OwnerId = random_user.id
            response = await client.post(f"{DOT_NET_API}/Discussion",
                                         json=discussion,
                                         headers={"Authorization": f"Bearer {random_user.token}"})
            if response.status_code == 200:
                discussion["id"] = response.json().get("id")
                create_discussion_to_db(discussion, db)
                list_discussions.append(discussion)
            else:
                raise HTTPException(status_code=response.status_code, detail=response.text)
    return list_discussions