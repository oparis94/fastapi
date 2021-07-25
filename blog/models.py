from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship

class Blogdb(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    creator = relationship("Userdb", back_populates="blogs")

class Userdb(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    blogs = relationship("Blogdb", back_populates="creator")
