from fastapi import HTTPException
from typing import List
import httpx
import os
from dotenv import load_dotenv
from app.models import User, Discussion
from app.CRUD.joining_crud import create_joining_to_db


load_dotenv()
DOT_NET_API = os.getenv("ASPNET_API_URL")

async def create_multiple_joining_to_discussion(users: List[User], discussions: Discussion, db) -> None:
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
            else:
                raise HTTPException(status_code=response.status_code, detail=response.text)
