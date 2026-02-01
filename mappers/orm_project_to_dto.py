from db.models.project import Project
from schemas.project import ProjectGet

# we do not need session as data is already fetched from db

def orm_project_to_dto(project: Project) -> ProjectGet:
    return ProjectGet(
        title=project.title,
        description=project.description,
        tech_stack=project.tech_stack
    )