from fastapi import APIRouter, Depends
from requests import Session
from app.services.post_services import populate_all_discussions_with_posts, populate_all_discussions_with_answers
from app.database import SessionLocal
def get_session_local():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
router = APIRouter()

@router.post("/generate")
async def create_questions_to_discussions(db: Session = Depends(get_session_local)):
    try:
        questions = await populate_all_discussions_with_posts(db)
        return {"questions": questions}
    except Exception as ex:
        return {"error": str(ex)}

@router.post("/answers/generate")
async def create_answers_to_discussions(db: Session = Depends(get_session_local)):
    try:
        answers = await populate_all_discussions_with_answers(db)
        return answers
    except Exception as ex:
        return {"error": str(ex)}