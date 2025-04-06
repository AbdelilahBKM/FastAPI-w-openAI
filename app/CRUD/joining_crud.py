from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Joining, User
from app.CRUD.user_crud import get_user_by_id


def create_joining_to_db(joining_data: dict, db: Session) -> None:
    db_joining = Joining(
        id=joining_data["id"],
        userId=joining_data["userId"],
        discussionId=joining_data["discussionId"]
    )
    db.add(db_joining)
    db.commit()


def get_all_joining(db: Session) -> list:
    return db.query(Joining).all()


def get_all_joining_by_discussion_id(discussion_id: int, db: Session) -> list[User]:
    return db.query(Joining).filter(Joining.discussionId == discussion_id).all()


def get_all_joining_by_user_id(user_id: str, db: Session) -> list:
    return db.query(Joining).filter(Joining.userId == user_id).all()


def get_random_user_by_discussion_id(discussion_id: int, db: Session) -> User | None:
    joining = db.query(Joining).filter(Joining.discussionId == discussion_id).order_by(func.random()).first()
    if joining:
        return get_user_by_id(db, joining.userId)
    return None
