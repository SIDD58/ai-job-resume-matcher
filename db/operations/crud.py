# db/crud.py
from sqlalchemy.orm import Session
from db.models.project import Project
from services.fingerprint import fingerprint
from services.embeddings import generate_embedding
from schemas.project import ProjectCreate

def store_project(session: Session, project_data:ProjectCreate ) -> str:
    fp = fingerprint(project_data.searchable_text)
    
    exists = session.query(Project).filter_by(fingerprint=fp).first()
    if exists:
        return "duplicate"

    embedding = generate_embedding(project_data.searchable_text)

    project = Project(
        title=project_data.title,
        description=project_data.description,
        tech_stack=project_data.tech_stack,
        searchable_text=project_data.searchable_text,
        embedding=embedding,
        fingerprint=fp,
        created_by=project_data.created_by
    )
    session.add(project)
    session.commit()
    return "stored"


def delete_projects(session: Session) -> str:
    session.query(Project).delete()
    session.commit()
    return "deleted"