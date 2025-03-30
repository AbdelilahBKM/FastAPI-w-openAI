from fastapi import FastAPI, Depends
from dotenv import load_dotenv
from app.database import SessionLocal
from sqlalchemy.orm import Session
from app.services.openai_api import generate_gpt_response
from app.services.user_services import generate_new_users, get_local_users

load_dotenv()
app = FastAPI()

@app.get("/ping")
async def root():
    return {"message": "Hello World"}

@app.get("/pingOpenAI")
async def pingOpenAI():
    try:
        response = generate_gpt_response("ping")
        return {"message": response}
    except Exception as ex:
        return {"error": str(ex)}

@app.post("/Users/generateUsers/{nbr_users}")
async def generate_users(nbr_users: int, db: Session = Depends(SessionLocal)):
    try:
        users = await generate_new_users(nbr_users, db)
        return {"users": users}
    except Exception as ex:
        return {"error": str(ex)}

@app.get("/Users")
async def get_users(db: Session = Depends(SessionLocal)):
    try:
        users = await get_local_users(db)
        return {"users": users}
    except Exception as ex:
        return {"error": str(ex)}
