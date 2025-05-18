from fastapi import APIRouter, Depends
from requests import Session

from app.CRUD.joining_crud import get_all_joining, get_all_joining_by_discussion_id, get_all_joining_by_user_id
from app.services.joining_services import create_joining_to_discussions
from app.database import SessionLocal
def get_session_local():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
router = APIRouter()

@router.get("/local/all")
async def get_joining(db: Session = Depends(get_session_local)):
    try:
        joining =  get_all_joining(db)
        return {"joining": joining}
    except Exception as ex:
        return {"error": str(ex)}

@router.get("/discussion/{discussion_id}")
async def get_joining_by_discussion(discussion_id: int, db: Session = Depends(get_session_local)):
    try:
        joining = get_all_joining_by_discussion_id(discussion_id, db)
        return {"joining": joining}
    except Exception as ex:
        return {"error": str(ex)}

@router.get("/user/{user_id}")
async def get_joining_by_user(user_id: str, db: Session = Depends(get_session_local)):
    try:
        joining = get_all_joining_by_user_id(user_id, db)
        return {"joining": joining}
    except Exception as ex:
        return {"error": str(ex)}

@router.post("/generate")
async def generate_joining(db: Session = Depends(get_session_local)):
    try:
        results = await create_joining_to_discussions(db)
        return {"joining": results}
    except Exception as ex:
        return {"error": str(ex)}