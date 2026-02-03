from db.base import Base
# import all models here so that they are registered with SQLAlchemy Base
from db.models.project import Project
from db.models.job import Job
from db.engine import engine

def init_db():
    Base.metadata.create_all(bind=engine)