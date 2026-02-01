# db/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

pg_user = os.environ["POSTGRES_USER"]
pg_password = quote_plus(os.environ["POSTGRES_PASSWORD"])
pg_host = os.environ["POSTGRES_HOST"]
pg_port = os.environ.get("POSTGRES_PORT", "5432")
pg_database = os.environ["POSTGRES_DB"]

DATABASE_URL = (
    f"postgresql+psycopg://{pg_user}:{pg_password}"
    f"@{pg_host}:{pg_port}/{pg_database}"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
