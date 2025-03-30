from typing import List

import httpx
import json
import os
from dotenv import load_dotenv
from app.models import User, Discussion, Joining


load_dotenv()
DOT_NET_API = os.getenv("ASPNET_API_URL")

async def create_multiple_joining_to_discussion(users: List[User], discussions: List[Discussion], db) -> None:
    for discussions in discussions:
        for user in users:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{DOT_NET_API}/Joining", headers={"Content-Type": "application/json", "Authorization": f"Bearer {user.token}"},)