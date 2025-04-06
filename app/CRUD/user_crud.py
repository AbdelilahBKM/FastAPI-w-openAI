from app.models import User
from sqlalchemy.orm import Session
import random


def add_user_to_db(user_data: dict, db: Session) -> None:
    db_user = User(
        id=user_data["id"],
        userName=user_data["userName"],
        firstName=user_data["firstName"],
        lastName=user_data["lastName"],
        email=user_data["email"],
        password=user_data["password"],
        token=user_data["token"]
        )
    db.add(db_user)
    db.commit()

def get_all_local_users(db: Session) -> list:
    return db.query(User).all()

def get_user_by_id(db: Session, user_id: str) -> User:
    return db.query(User).filter(User.id == user_id).first()

def get_random_user(db: Session) -> User:
    users = db.query(User).all()
    return random.choice(users) if users else None

def get_random_users(db: Session, count: int) -> list:
    users = db.query(User).all()
    return random.sample(users, count) if len(users) >= count else users
