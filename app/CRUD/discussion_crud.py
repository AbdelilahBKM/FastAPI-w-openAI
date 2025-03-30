from app.models import Discussion
from sqlalchemy import Session

def create_discussion_to_db(discussion_data: dict, db: Session) -> None:
    db_discussion = Discussion(
        d_Name=discussion_data["d_Name"],
        d_Profile=discussion_data["d_Profile"],
        d_Description=discussion_data["d_Description"],
        OwnerId=discussion_data["OwnerId"]
    )
    db.add(db_discussion)
    db.commit()