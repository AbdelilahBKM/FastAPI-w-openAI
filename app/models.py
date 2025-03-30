from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True, index=True)
    userName = Column(String, index=True)
    firstName = Column(String, index=True)
    lastName = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, index=True)
    token = Column(String)

class Discussion(Base):
    __tablename__ = 'discussions'
    id = Column(Integer, primary_key=True, index=True)
    d_Name = Column(String, index=True)
    d_Profile = Column(String, index=True)
    d_Description = Column(String, index=True, default="description")
    OwnerId = Column(String, foreign_key=True, index=True, references='users.id')

class Joining(Base):
    __tablename__ = 'joinings'
    id = Column(Integer, primary_key=True, index=True)
    userId = Column(String, foreign_key=True, index=True, references='users.id')
    discussionId = Column(Integer, foreign_key=True, index=True, references='discussions.id')

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String, index=True)
    postedBy = Column(String, foreign_key=True, index=True, references='users.id')
    questionId = Column(Integer, foreign_key=True, index=True, references='questions.id', nullable=True)
    discussionId = Column(Integer, foreign_key=True, index=True, references='discussions.id', nullable=True)
    postType = Column(Integer, index=True) # 0 for question, 1 for answer

class Vote(Base):
    __tablename__ = 'votes'
    id = Column(Integer, primary_key=True, index=True)
    userId = Column(String, foreign_key=True, index=True, references='users.id')
    postId = Column(Integer, foreign_key=True, index=True, references='posts.id')
    voteType = Column(Integer, index=True) # 1 for downvote, 0 for upvote