from secrets import token_hex
import uuid

from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException

from sqlalchemy.orm import Session
from pydantic import parse_obj_as

from database import engine, SessionLocal
from schemas import UserBase, User, UserCreate
from models import Base


Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/add_user/")
def add_user(user: UserBase) -> User:
    user_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, name=user.username)
    print(type(user_uuid))
    user_create_time = datetime.now().isoformat()
    print(user_create_time)
    token = token_hex(32)
    print(token)
    user = User(
        username=user.username,
        uuid=user_uuid,
        token=token,
        created_at=user_create_time
    )
    return user 
