from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
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

    # Relationships
    discussions = relationship("Discussion", back_populates="owner")
    joinings = relationship("Joining", back_populates="user")
    posts = relationship("Post", back_populates="posted_by_user")
    votes = relationship("Vote", back_populates="user")


class Discussion(Base):
    __tablename__ = 'discussions'
    id = Column(Integer, primary_key=True, index=True)
    d_Name = Column(String, index=True)
    d_Profile = Column(String, index=True)
    d_Description = Column(String, index=True, default="description")
    OwnerId = Column(String, ForeignKey('users.id'), index=True)  # Corrected foreign key
    # Relationships
    owner = relationship("User", back_populates="discussions")
    joinings = relationship("Joining", back_populates="discussion")
    posts = relationship("Post", back_populates="discussion")


class Joining(Base):
    __tablename__ = 'joinings'
    id = Column(Integer, primary_key=True, index=True)
    userId = Column(String, ForeignKey('users.id'), index=True)  # Corrected
    discussionId = Column(Integer, ForeignKey('discussions.id'), index=True)  # Corrected

    # Relationships
    user = relationship("User", back_populates="joinings")
    discussion = relationship("Discussion", back_populates="joinings")


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String, index=True)
    postedBy = Column(String, ForeignKey('users.id'), index=True)  # Corrected
    questionId = Column(Integer, ForeignKey('posts.id'), nullable=True)  # Changed from 'questions.id'
    discussionId = Column(Integer, ForeignKey('discussions.id'), nullable=True)  # Corrected
    postType = Column(Integer, index=True)  # 0 for question, 1 for answer

    # Relationships
    posted_by_user = relationship("User", back_populates="posts")
    discussion = relationship("Discussion", back_populates="posts")
    votes = relationship("Vote", back_populates="post")
    answers = relationship("Post", remote_side=[id])  # For question-answer relationship


class Vote(Base):
    __tablename__ = 'votes'
    id = Column(Integer, primary_key=True, index=True)
    userId = Column(String, ForeignKey('users.id'), index=True)  # Corrected
    postId = Column(Integer, ForeignKey('posts.id'), index=True)  # Corrected
    voteType = Column(Integer, index=True)  # 1 for downvote, 0 for upvote

    # Relationships
    user = relationship("User", back_populates="votes")
    post = relationship("Post", back_populates="votes")