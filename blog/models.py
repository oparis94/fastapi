from sqlalchemy import Column, String, Integer, Boolean
from .database import Base

class Blogdb(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
