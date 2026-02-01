from db.base import Base
from db.models.project import Project
from db.engine import engine

def init_db():
    Base.metadata.create_all(bind=engine)