from fastapi import FastAPI, Depends
from dotenv import load_dotenv
from fastapi import Request

from app.CRUD.discussion_crud import get_local_discussions
from app.CRUD.joining_crud import (get_all_joining, get_all_joining_by_discussion_id,
                                   get_all_joining_by_user_id)
from app.database import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.services.discussion_services import get_all_discussions_asp
from app.services.joining_services import create_joining_to_discussions
from app.services.openai_api import generate_gpt_response
from app.services.user_services import generate_new_users, get_local_users
from app.services.discussion_services import create_discussions_asp, create_discussion_asp
from app.services.post_services import (populate_all_discussions_with_posts,
                                        populate_all_discussions_with_answers)
from app.utils.functions import discussions

def get_session_local():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



load_dotenv()
app = FastAPI()

@app.on_event("startup")
async def test_db_connection():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        print("✅ Database connection successful")
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")

@app.get("/ping")
async def root():
    return {"message": "Hello World"}

@app.get("/pingOpenAI")
async def ping_openai():
    try:
        response = generate_gpt_response("ping")
        return {"message": response}
    except Exception as ex:
        return {"error": str(ex)}

@app.post("/OpenAI/request")
async def create_openai_request(request: Request):
    try:
        body = await request.json()
        response = generate_gpt_response(body["prompt"])
        return {"message": response}
    except Exception as ex:
        return {"error": str(ex)}

@app.post("/Users/generateUsers/{nbr_users}")
async def generate_users(
        nbr_users: int,
        db: Session = Depends(get_session_local)):
    print(f"Received request with nbr_users: {nbr_users}")
    try:
        users = await generate_new_users(nbr_users, db)
        return {"users": users}
    except Exception as ex:
        return {"error": str(ex)}

@app.get("/Users")
async def get_users(db: Session = Depends(get_session_local)):
    try:
        users = await get_local_users(db)
        return {"users": users}
    except Exception as ex:
        return {"error": str(ex)}


@app.get("/Discussions/local")
async def get_discussions(db: Session = Depends(get_session_local)):
    try:
        local_discussions = get_local_discussions(db)
        return {"discussions": local_discussions}
    except Exception as ex:
        return {"error": str(ex)}

@app.get("/Discussions/asp")
async def get_discussions_asp(db: Session = Depends(get_session_local)):
    try:
        external_discussions = await get_all_discussions_asp(db)
        return {"discussions": external_discussions}
    except Exception as ex:
        return {"error": str(ex)}

@app.post("/Discussions/generate")
async def generate_discussions(db: Session = Depends(get_session_local)):
    try:
        discussion = await create_discussions_asp(discussions, db)
        return {"discussions": discussion}
    except Exception as ex:
        return {"error": str(ex)}

@app.post("/Discussions/new")
async def create_discussion(request: Request, db: Session = Depends(get_session_local)):
    try:
        body = await request.json()
        discussion = await create_discussion_asp(body["discussion"], db)
        return {"discussion": discussion}
    except Exception as ex:
        return {"error": str(ex)}

@app.get("/Joining")
async def get_joining(db: Session = Depends(get_session_local)):
    try:
        joining =  get_all_joining(db)
        return {"joining": joining}
    except Exception as ex:
        return {"error": str(ex)}

@app.get("/Joining/discussion/{discussion_id}")
async def get_joining_by_discussion(discussion_id: int, db: Session = Depends(get_session_local)):
    try:
        joining = get_all_joining_by_discussion_id(discussion_id, db)
        return {"joining": joining}
    except Exception as ex:
        return {"error": str(ex)}

@app.get("/Joining/user/{user_id}")
async def get_joining_by_user(user_id: str, db: Session = Depends(get_session_local)):
    try:
        joining = get_all_joining_by_user_id(user_id, db)
        return {"joining": joining}
    except Exception as ex:
        return {"error": str(ex)}

@app.post("/Joining/generate")
async def generate_joining(db: Session = Depends(get_session_local)):
    try:
        results = await create_joining_to_discussions(db)
        return {"joining": results}
    except Exception as ex:
        return {"error": str(ex)}

@app.post("/Post/generate")
async def create_questions_to_discussions(db: Session = Depends(get_session_local)):
    try:
        questions = await populate_all_discussions_with_posts(db)
        return {"questions": questions}
    except Exception as ex:
        return {"error": str(ex)}

@app.post("/Post/answers/generate")
async def create_answers_to_discussions(db: Session = Depends(get_session_local)):
    try:
        answers = await populate_all_discussions_with_answers(db)
        return answers
    except Exception as ex:
        return {"error": str(ex)}
