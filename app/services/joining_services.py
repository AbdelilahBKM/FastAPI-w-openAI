from fastapi import HTTPException
from typing import List
import httpx
import os
import random
from dotenv import load_dotenv
from app.models import Discussion
from app.CRUD.joining_crud import create_joining_to_db
from app.CRUD.user_crud import get_random_users
from app.CRUD.discussion_crud import get_local_discussions

load_dotenv()
DOT_NET_API = os.getenv("ASPNET_API_URL")


async def create_multiple_joining_to_discussion(discussion: Discussion, db) -> List[dict]:
    users = get_random_users(db, random.randint(7, 25))
    print(len(users))
    joinings: List[dict] = []

    async with httpx.AsyncClient(verify=False) as client:
        for user in users:
            try:
                joining_payload = {
                    "userId": str(user.id),
                    "discussionId": discussion.id
                }
                print(f"*** JOINING PAYLOAD: {joining_payload} ***")
                response = await client.post(
                    f"{DOT_NET_API}/Joining",
                    headers={
                        "Content-Type": "application/json"
                    },
                    json=joining_payload
                )
                if response.status_code in (200, 201):
                    joining_data = response.json()
                    joinings.append({
                        "id": joining_data["id"],
                        "user_id": user.id,
                        "discussion_id": discussion.id
                    })
                    create_joining_to_db({
                        "id": joining_data["id"],
                        "userId": user.id,
                        "discussionId": discussion.id
                    }, db)
                else:
                    print(
                        f"Failed to create joining for user {user.id}. Status: {response.status_code}, Response: {response.text}")

            except Exception as e:
                print(f"Error creating joining for user {user.id}: {str(e)}")
                # continue
    return joinings

async def create_joining_to_discussions(db) -> List[dict] | None:
    discussions = get_local_discussions(db)
    joining_list: List[dict] = []
    for discussion in discussions:
        joining = await create_multiple_joining_to_discussion(discussion, db)
        print(joining)
        if joining:
            joining_list.append({
                "discussion_id": discussion.id,
                "joining": joining
            })
    return joining_list