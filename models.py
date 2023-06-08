from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    uuid = Column(String, primary_key=True, index=True)
    username = Column(String)
    token = Column(String, unique=True)
    created_at = Column(DateTime)
