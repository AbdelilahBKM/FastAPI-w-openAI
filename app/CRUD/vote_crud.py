from sqlalchemy.orm import Session
from app.models import Vote

def create_vote_to_db(vote: Vote, db: Session) -> None:
    db.session.add(vote)
    db.session.commit()