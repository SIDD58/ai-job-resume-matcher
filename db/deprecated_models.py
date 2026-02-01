#from sqlalchemy.ext.declarative import declarative_base
#Base=declarative_base()
from db.base import Base
from sqlalchemy import Column, Text, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID,ARRAY
from pgvector.sqlalchemy import Vector
import uuid
from datetime import datetime


# Project Model 
class Project(Base):
    __tablename__ = "projects"
    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    title=Column(Text,nullable=False)
    description=Column(Text,nullable=False)
    tech_stack=Column(ARRAY(Text))
    searchable_text=Column(Text,nullable=False)
    embedding=Column(Vector(1536))
    fingerprint = Column(Text, unique=True, nullable=False)
    created_by = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


# # Testing to create a project 
# new_project = Project(
#     title="My Awesome Project",
#     description="A project demonstrating SQLAlchemy mapping.",
#     tech_stack=["Python", "SQLAlchemy", "PostgreSQL"],
#     searchable_text="This project is all about demonstrating how to map a database schema to a Python object using SQLAlchemy.",
#     fingerprint="unique-fingerprint-12345",
#     created_by="user@example.com"
# )





