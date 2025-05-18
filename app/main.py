from fastapi import FastAPI
from dotenv import load_dotenv
from app.database import SessionLocal
from sqlalchemy import text
from app.routers import (openai_routes, user_routes,
                         discussion_routes, joining_routes,
                         post_routes, cross_encoder_routes)
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
app.include_router(openai_routes.router, prefix="/openai")
app.include_router(user_routes.router, prefix="/users")
app.include_router(discussion_routes.router, prefix="/discussions")
app.include_router(joining_routes.router, prefix="/joining")
app.include_router(post_routes.router, prefix="/post")
app.include_router(cross_encoder_routes.router, prefix="/cross-encoder")