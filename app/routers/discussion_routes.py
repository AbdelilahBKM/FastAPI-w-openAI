from fastapi import APIRouter, Request, Depends
from requests import Session

from app.CRUD.discussion_crud import get_local_discussions
from app.services.discussion_services import create_discussions_asp, create_discussion_asp, get_all_discussions_asp
from app.utils.functions import discussions
from app.database import SessionLocal
def get_session_local():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

@router.get("/local/all")
async def get_discussions(db: Session = Depends(get_session_local)):
    try:
        local_discussions = get_local_discussions(db)
        return {"discussions": local_discussions}
    except Exception as ex:
        return {"error": str(ex)}

@router.get("/asp/all")
async def get_discussions_asp(db: Session = Depends(get_session_local)):
    try:
        external_discussions = await get_all_discussions_asp(db)
        return {"discussions": external_discussions}
    except Exception as ex:
        return {"error": str(ex)}

@router.post("/generate")
async def generate_discussions(db: Session = Depends(get_session_local)):
    try:
        discussion = await create_discussions_asp(discussions, db)
        return {"discussions": discussion}
    except Exception as ex:
        return {"error": str(ex)}

@router.post("/new")
async def create_discussion(request: Request, db: Session = Depends(get_session_local)):
    try:
        body = await request.json()
        discussion = await create_discussion_asp(body["discussion"], db)
        return {"discussion": discussion}
    except Exception as ex:
        return {"error": str(ex)}