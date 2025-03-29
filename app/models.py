from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True, index=True)
    username = Column(String, index=True)   
    firstName = Column(String, index=True)
    lastName = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, index=True)
    token = Column(String)
