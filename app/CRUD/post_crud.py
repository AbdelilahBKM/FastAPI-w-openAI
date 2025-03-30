from app.models import Post
from sqlalchemy import Session

def create_question_to_db(question_data: dict, db: Session) -> None:
    db_question = Post(
        title=question_data["title"],
        content=question_data["content"],
        postedBy=question_data["postedBy"],
        discussionId=question_data["discussionId"],
        postType=0
    )
    db.add(db_question)
    db.commit()

def create_answer_to_db(answer_data: dict, db: Session) -> None:
    db_answer = Post(
        title=answer_data["title"],
        content=answer_data["content"],
        postedBy=answer_data["postedBy"],
        questionId=answer_data["questionId"],
        postType=1
    )
    db.add(db_answer)
    db.commit()