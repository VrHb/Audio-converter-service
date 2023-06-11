import os
import uuid
from uuid import UUID
from secrets import token_hex
from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException, File, UploadFile

from sqlalchemy.orm import Session
from pydantic import parse_obj_as

from pydub import AudioSegment

from database import engine, SessionLocal
from schemas import UserBase, User, UserCreate
from models import Base



BASE_DIR = os.path.dirname(__file__)
Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def convert_file(audiofile: UploadFile) -> UUID:
    wav_file_path = os.path.join(BASE_DIR, audiofile.filename)
    with open(wav_file_path, "bw") as file_object:
        audio = file_object.write(audiofile.file.read())
    audio = AudioSegment.from_file(wav_file_path, format="wav")
    os.remove(wav_file_path)
    new_filename = f"{audiofile.filename.split('.')[0]}.mp3"
    audio.export(os.path.join(BASE_DIR, new_filename), format="mp3")

    audiofile_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, name=audiofile.filename)
    return audiofile_uuid


@app.post("/add_user/")
def add_user(user: UserBase) -> User:
    user_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, name=user.username)
    user_create_time = datetime.now().isoformat()
    token = token_hex(32)
    user = User(
        username=user.username,
        uuid=user_uuid,
        token=token,
        created_at=user_create_time
    )
    return user 


@app.post("/convert_audio/")
def convert_audio(user_uuid: str, token: str, audiofile: UploadFile) -> UUID | str:
    if audiofile.content_type != "audio/wav":
        return "Wrong file format!"
    audiofile_uuid = convert_file(audiofile)
    return audiofile_uuid

