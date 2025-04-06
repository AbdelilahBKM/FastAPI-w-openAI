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
        async with httpx.AsyncClient(verify=False) as client:
            random_user = get_random_user(db)
            discussion.OwnerId = random_user.id
            response = await client.post(f"{DOT_NET_API}/Discussion",
                                         headers={
                                             "Content-Type": "application/json"},
                                         json={
                                              "d_Name": discussion.d_Name,
                                              "d_Description": discussion.d_Description,
                                              "d_Profile": discussion.d_Profile,
                                              "ownerId": discussion.OwnerId
                                        })
            if response.status_code in (200, 201):
                data_json = response.json()
                discussion.id= data_json["id"]
            else:
                raise HTTPException(status_code=response.status_code, detail=response.text)
        create_discussion_to_db(discussion, db)
        list_discussions.append(discussion)
    return list_discussions

async def get_all_discussions_asp(db) -> List[Discussion]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{DOT_NET_API}/Discussion")
        if response.status_code == 200:
            discussions = response.json()
            for discussion in discussions:
                discussion["id"] = discussion.pop("id")
                create_discussion_to_db(discussion, db)
            return discussions
        raise HTTPException(status_code=response.status_code, detail=response.text)
