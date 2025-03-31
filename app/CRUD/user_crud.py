from app.models import User
from sqlalchemy import Session
import random


async def add_user_to_db(user_data: dict, db: Session) -> None:
    db_user = User(
        userName=user_data["userName"],
        firstName=user_data["firstName"],
        lastName=user_data["firstName"],
        email=user_data["firstName"],
        password=user_data["password"],
        token=user_data["token"]
        )
    db.add(db_user)
    await db.commit()

async def get_all_local_users(db: Session) -> list:
    return await db.query(User).all()

async def get_user_by_id(db: Session, user_id: str) -> User:
    return await db.query(User).filter(User.id == user_id).first()

async def get_random_user(db: Session) -> User:
    users = await db.query(User).all()
    return random.choice(users) if users else None

async def get_random_users(db: Session, count: int) -> list:
    users = await db.query(User).all()
    return random.sample(users, count) if len(users) >= count else users
