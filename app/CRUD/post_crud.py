from app.models import Post
from sqlalchemy.orm import Session

def create_question_to_db(question_data: dict, db: Session) -> Post:
    db_question = Post(
        title=question_data["title"],
        content=question_data["content"],
        postedBy=question_data["postedBy"],
        discussionId=question_data["discussionId"],
        postType=0
    )
    db.add(db_question)
    db.commit()
    return db_question

def get_question_by_id(question_id: int, db: Session) -> Post | None:
    return db.query(Post).filter(Post.id == question_id, Post.postType == 0).first()

def get_questions_by_discussion_id(discussion_id: int, db: Session) -> list[Post] | None:
    return db.query(Post).filter(Post.discussionId == discussion_id, Post.postType == 0).all()

def get_answer_by_id(answer_id: int, db: Session) -> Post | None:
    return db.query(Post).filter(Post.id == answer_id, Post.postType == 1).first()

def create_answer_to_db(answer_data: dict, db: Session) -> Post:
    db_answer = Post(
        title=answer_data["title"],
        content=answer_data["content"],
        postedBy=answer_data["postedBy"],
        questionId=answer_data["questionId"],
        postType=1
    )
    db.add(db_answer)
    db.commit()
    return db_answer