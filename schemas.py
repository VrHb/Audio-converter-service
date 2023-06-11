from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class Song(BaseModel):
    uuid: UUID
    file_path: str
    user_id: int 

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    uuid: UUID | int 
    token: str
    songs: list[Song] = []

    class config:
        orm_mode = True
