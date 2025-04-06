from fastapi import HTTPException
import httpx
from typing import List
from app.utils.functions import generate_user
from app.CRUD.user_crud import add_user_to_db, get_all_local_users
from dotenv import load_dotenv
import os
load_dotenv()
DOT_NET_API = os.getenv("ASPNET_API_URL")

async def get_local_users(db) -> List[dict]:
        return get_all_local_users(db)

async def generate_new_users(nbr_users: int, db) -> List[dict]:
    list_users = generate_user(nbr_users)
    print(list_users)
    counter = 0
    for user in list_users:
        counter += 1
        async with httpx.AsyncClient(verify=False) as client:
            print("Sending request to .NET API " + DOT_NET_API)
            print(f"Registering user:  {counter}")
            response = await client.post(f"{DOT_NET_API}/UserIdentity/Register", json=user)
            if response.status_code == 200:
                response_json = response.json()
                user["id"] = response_json["user"]["id"]
                user["token"] = response_json["token"]
            else:
                raise HTTPException(status_code=response.status_code, detail=response.text)
        add_user_to_db(user, db)

    return list_users