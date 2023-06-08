import os

from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


load_dotenv()

PSQL_PASSWORD = os.getenv("PSQL_PASSWORD")
PSQL_PORT = os.getenv("PSQL_PORT", default="5432")

DATABASE_URL = f"postgresql://postgres:{PSQL_PASSWORD}@localhost:{PSQL_PORT}"

engine = create_engine(
    DATABASE_URL 
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

