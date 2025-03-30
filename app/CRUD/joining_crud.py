from sqlalchemy import Session
from app.models import Joining


def create_joining_to_db(joining_data: dict, db: Session) -> None:
    db_joining = Joining(
        userId=joining_data["userId"],
        discussionId=joining_data["discussionId"]
    )
    db.add(db_joining)
    db.commit()