from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    uuid: UUID | int 
    token: str
    created_at: datetime

    class config:
        orm_mode = True
