from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import DATABASE_URL

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine, #refers to the engine created above
    autoflush=False, # will not flush changes automatically
    autocommit=False # will not commit changes automatically
)