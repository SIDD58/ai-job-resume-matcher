from schemas.project import ProjectCreate as Project
from typing import List, Dict, Union
ProjectDict = Dict[str, Union[str, List[str]]]

def noramlize_project(data:Project)->ProjectDict:
    title=data.title.strip().lower()
    description=data.description.strip().lower()
    tech_stack= [tech.lower() for tech in data.tech_stack]
    created_by=data.created_by
    searchable_text=(
        f"title: {title}, "
        f"description: {description}, "
        f"tech_stack: {tech_stack} "
    )

    return{
    "title": title,
    "description": description,
    "tech_stack": tech_stack,
    "searchable_text":searchable_text,
    "created_by": created_by
}
