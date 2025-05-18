from fastapi import APIRouter, Depends
from requests import Session
from app.services.user_services import generate_new_users, get_local_users
from app.database import SessionLocal
def get_session_local():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
router = APIRouter()
@router.post("/generateUsers/{nbr_users}")
async def generate_users(
        nbr_users: int,
        db: Session = Depends(get_session_local)):
    print(f"Received request with nbr_users: {nbr_users}")
    try:
        users = await generate_new_users(nbr_users, db)
        return {"users": users}
    except Exception as ex:
        return {"error": str(ex)}

@router.get("/local/all")
async def get_users(db: Session = Depends(get_session_local)):
    try:
        users = await get_local_users(db)
        return {"users": users}
    except Exception as ex:
        return {"error": str(ex)}