from fastapi import FastAPI
from pydantic import BaseModel
from models import personalizedContentRec
import torch

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# # @app.get("/hello/{name}")
# # async def say_hello(name: str):
# #     return {"message": f"Hello {name}"}
# class UserQuery(BaseModel):
#     user_id: int
#     history: list[str]
#
# @app.post('/PersonalizedContentRec')
# async def recommande(query: UserQuery):
#     pass