from sqlalchemy.orm import Session


from models import User, Song 
from schemas import UserCreate


def get_user(db: Session, uuid: str, token: str):
    return db.query(User).filter(User.uuid == uuid, User.token == token).first()


def get_song(db: Session, song_id: int, user_id: int):
    return db.query(Song).filter(Song.id == song_id, Song.user_id == user_id).first()


def create_user(db: Session, user: UserCreate):
    db_user = User(
        username=user.username,
        uuid=user.uuid,
        token=user.token,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_song(db: Session, song: Song):
    db_song = Song(
        uuid=song.uuid,
        user_id=song.user_id,
        file_path=song.file_path
    )
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return db_song
