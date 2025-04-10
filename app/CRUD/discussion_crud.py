from app.models import Discussion
from sqlalchemy.orm import Session

def create_discussion_to_db(db_discussion, db: Session) -> None:
    db.add(db_discussion)
    db.commit()

def get_local_discussions(db: Session) -> list:
    return db.query(Discussion).all()

def get_discussion_by_id(discussion_id: int, db: Session) -> Discussion:
    return db.query(Discussion).filter(Discussion.id == discussion_id).first()