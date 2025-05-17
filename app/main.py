from fastapi import FastAPI, Depends, HTTPException, Request
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

from app.CRUD.discussion_crud import get_local_discussions
from app.CRUD.joining_crud import (get_all_joining, get_all_joining_by_discussion_id,
                                   get_all_joining_by_user_id)
from app.database import SessionLocal
from app.services.discussion_services import get_all_discussions_asp, create_discussions_asp, create_discussion_asp
from app.services.joining_services import create_joining_to_discussions
from app.services.openai_api import generate_gpt_response
from app.services.user_services import generate_new_users, get_local_users
from app.services.post_services import (populate_all_discussions_with_posts,
                                       populate_all_discussions_with_answers)
from app.services.ai_services import (generate_grok_response, detect_duplicate_post,
                                     get_chatbot_response, get_personalized_recommendations)
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
async def startup_event():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        print("✅ Database connection successful")
        # Initialize conversation_history table for chatbot
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS conversation_history (
                session_id VARCHAR(50) PRIMARY KEY,
                user_id VARCHAR(50),
                history TEXT,
                created_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """))
        db.commit()
        print("✅ Conversation history table initialized")
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
    finally:
        db.close()

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
async def generate_users(nbr_users: int, db: Session = Depends(get_session_local)):
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
        joining = get_all_joining(db)
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
        return {"answers": answers}
    except Exception as ex:
        return {"error": str(ex)}

# New Endpoints for AI Features
class PostRequest(BaseModel):
    user_id: str
    discussion_id: int
    content: str

class ChatRequest(BaseModel):
    session_id: Optional[str]
    user_id: str
    message: str

class RecommendationRequest(BaseModel):
    user_id: str

@app.post("/Post/suggest-answer")
async def suggest_answer(request: PostRequest, db: Session = Depends(get_session_local)):
    try:
        # Generate AI suggestion using xAI Grok
        suggestion = await generate_grok_response(
            prompt=f"You are a programming expert. Provide a concise and accurate answer to the following question:\n{request.content}",
            max_tokens=150
        )
        # Save post and AI suggestion
        post = {
            "discussion_id": request.discussion_id,
            "user_id": request.user_id,
            "content": request.content,
            "is_answer": False,
            "created_at": datetime.utcnow()
        }
        db.execute(text("""
            INSERT INTO posts (discussion_id, user_id, content, is_answer, created_at)
            VALUES (:discussion_id, :user_id, :content, :is_answer, :created_at)
        """), post)
        suggestion_post = {
            "discussion_id": request.discussion_id,
            "user_id": "ai-bot",
            "content": suggestion,
            "is_answer": True,
            "created_at": datetime.utcnow()
        }
        db.execute(text("""
            INSERT INTO posts (discussion_id, user_id, content, is_answer, created_at)
            VALUES (:discussion_id, :user_id, :content, :is_answer, :created_at)
        """), suggestion_post)
        db.commit()
        return {"suggestion": suggestion}
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(ex))

@app.post("/Post/detect-duplicate")
async def detect_duplicate(request: PostRequest, db: Session = Depends(get_session_local)):
    try:
        # Fetch existing posts (questions only)
        result = db.execute(text("SELECT content FROM posts WHERE is_answer = 0"))
        existing_questions = [row[0] for row in result.fetchall()]
        # Detect duplicate
        result = detect_duplicate_post(request.content, existing_questions)
        return result
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@app.post("/Chat")
async def chat(request: ChatRequest, db: Session = Depends(get_session_local)):
    try:
        response, session_id = await get_chatbot_response(
            session_id=request.session_id,
            user_id=request.user_id,
            message=request.message,
            db=db
        )
        return {"message": response, "session_id": session_id}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))

@app.post("/Recommendations")
async def get_recommendations(request: RecommendationRequest, db: Session = Depends(get_session_local)):
    try:
        recommendations = await get_personalized_recommendations(request.user_id, db)
        return {"recommendations": recommendations}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))