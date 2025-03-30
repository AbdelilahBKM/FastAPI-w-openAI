from sqlalchemy import Session
from app.models import Joining

def create_joining_to_db(joining_data: dict, db: Session) -> None:
    db_joining = Joining(
        userId=joining_data["userId"],
        discussionId=joining_data["discussionId"]
    )
    db.add(db_joining)
    db.commit()

def get_all_joining_by_discussion_id(db: Session, discussion_id: str) -> list:
    return  db.query(Joining).filter(Joining.discussionId == discussion_id).all()

def get_all_joining_by_user_id(db: Session, user_id: str) -> list:
    return db.query(Joining).filter(Joining.userId == user_id).all()
