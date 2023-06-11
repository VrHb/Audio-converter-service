import os
import uuid
from uuid import UUID
from secrets import token_hex
from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Request
from fastapi.responses import FileResponse
from pydantic.types import FilePath

from sqlalchemy.orm import Session
from pydantic import parse_obj_as, AnyUrl

from pydub import AudioSegment

from database import engine, SessionLocal
from schemas import UserBase, User, UserCreate, Song
from models import Base
from crud import create_user, get_user, get_song, create_song



BASE_DIR = os.path.dirname(__file__)
Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def convert_file(audiofile: UploadFile) -> str:
    wav_file_path = os.path.join(BASE_DIR, audiofile.filename)
    with open(wav_file_path, "bw") as file_object:
        audio = file_object.write(audiofile.file.read())
    audio = AudioSegment.from_file(wav_file_path, format="wav")
    os.remove(wav_file_path)
    new_filename = f"{audiofile.filename.split('.')[0]}.mp3"
    output_file_path = os.path.join(BASE_DIR, new_filename)
    audio.export(output_file_path, format="mp3")
    return output_file_path 


@app.get("/record/{user_id}/{song_id}")
def get_user_song(song_id: int, user_id: int, db: Session = Depends(get_db)) -> FileResponse:
    song = get_song(db=db, song_id=song_id, user_id=user_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found!")
    return FileResponse(song.file_path)


@app.post("/add_user/")
def add_user(user: UserBase, db: Session = Depends(get_db)) -> User:
    user_uuid = uuid.uuid5(uuid.NAMESPACE_URL, name=user.username)
    token = token_hex(32)
    validated_user = User(
        username=user.username,
        uuid=user_uuid,
        token=token,
    )
    create_user(db=db, user=validated_user)
    return validated_user 


@app.post("/convert_audio/")
def convert_audio(user_uuid: str, user_token: str, audiofile: UploadFile, db: Session = Depends(get_db), request: Request = None) -> AnyUrl | str:
    user_from_db = get_user(db=db, uuid=user_uuid, token=user_token)
    if not user_from_db:
        raise HTTPException(status_code=404, detail="User not found!")
    if audiofile.content_type != "audio/wav":
        raise HTTPException(status_code=404, detail="Wrong file format!")
    song_uuid = uuid.uuid5(uuid.NAMESPACE_URL, name=(audiofile.filename + user_uuid))
    file_path = convert_file(audiofile)
    song = Song(
        uuid=song_uuid,
        user_id=user_from_db.id,
        file_path=file_path
    )
    song_from_db = create_song(db=db, song=song) 
    return request.url_for(
        "get_user_song",
        user_id=user_from_db.id,
        song_id=song_from_db.id
    )._url 

