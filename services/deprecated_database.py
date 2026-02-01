from sqlalchemy import create_engine
from dotenv import load_dotenv
from urllib.parse import quote_plus
import hashlib,uuid
from datetime import datetime
from sqlalchemy import Column, Text, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import declarative_base, Session
from pgvector.sqlalchemy import Vector
from openai import OpenAI
import os

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIM = 1536

load_dotenv()
Base = declarative_base()
class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    tech_stack = Column(ARRAY(Text))
    searchable_text = Column(Text, nullable=False)
    embedding = Column(Vector(1536))
    fingerprint = Column(Text, unique=True, nullable=False)
    created_by = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

pg_user=os.environ['POSTGRES_USER']
pg_password:str=quote_plus(os.environ['POSTGRES_PASSWORD'])
pg_host=os.environ['POSTGRES_HOST']
pg_port=os.environ.get('POSTGRES_PORT','5432')
pg_database=os.environ['POSTGRES_DB']

DATABASE_URL = f"postgresql+psycopg://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_database}"

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

def store_project(session: Session, project_data: dict):
    fp = fingerprint(project_data["searchable_text"])

    #Checking whether record already exist or not 
    exists = session.query(Project).filter_by(fingerprint=fp).first()
    if exists:
        return "duplicate"

    embedding = generate_embedding(project_data["searchable_text"])

    project = Project(
        title=project_data["title"],
        description=project_data["description"],
        tech_stack=project_data["tech_stack"],
        searchable_text=project_data["searchable_text"],
        embedding=embedding,
        fingerprint=fp,
        created_by=project_data["created_by"]
    )

    session.add(project)
    session.commit()
    return "stored"

def generate_embedding(text: str) -> list[float]:

    if not text or not text.strip():
        raise ValueError("Text for embedding cannot be empty")

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )

    embedding = response.data[0].embedding

    # Safety check
    if len(embedding) != EMBEDDING_DIM:
        raise RuntimeError("Embedding dimension mismatch")
    return embedding


# Helper genrator functions for some fields 
def fingerprint(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()

