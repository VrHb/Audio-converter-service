from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, unique=True)
    username = Column(String)
    token = Column(String, unique=True)

    songs = relationship("Song", back_populates="user")

class Song(Base):
    __tablename__ = "songs"
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    file_path = Column(String)

    user = relationship("User", back_populates="songs")
