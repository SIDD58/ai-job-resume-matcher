from fastapi import APIRouter, Depends
from mappers.orm_project_to_dto import orm_project_to_dto
from schemas.project import ProjectCreate,ProjectGet
from schemas.job import JobCreate
from db.operations.crud import store_project,delete_projects
from db.operations.similarity import similar_project
from db.session import get_db
from typing import List, Dict, Union
ProjectDict = Dict[str, Union[str, List[str]]]
router = APIRouter()

@router.post('/add-project')
def post_project(data:ProjectCreate, session=Depends(get_db)):
    print("How does the Posted Data Looks like: ")
    print(data)
    result = store_project(session, data)
    print("Result of Storing Project: ", result)
    return {
        'project':data
    }


@router.post('/find-project')

# field names that you get in post data and pydantic model should match 

# if you do not provide tpe hint for the aergument in find_prject function , then fastapi will not treat it as json body and will treat it as query parameter
def find_project(data:JobCreate, session=Depends(get_db),response_model=List[ProjectGet]):
    print("How does the Posted Data Looks like: ")
    print(data)
    project_list=similar_project(session, data)
    orm_project_list: list[ProjectGet] = [orm_project_to_dto(proj) for proj in project_list]
    print("Similar Projects Found: ", orm_project_list)
    # return {
    #     'job':project_list # SQLAlchemy ORM objects are NOT JSON serializable. So, we need to convert them to dicts or use Pydantic models for response.
    # }
    #ORM models ≠ API response models
    return orm_project_list

@router.get('/projects')
def get_projects():
    return {
        "This will return all projects"
    }

@router.delete('/delete-projects')
def delete_projects_api(session=Depends(get_db)):
    result=delete_projects(session)
    print("Result of Deleting Projects: ", result)
    return {
        "status": result
    }

@router.post('/add-jd')
def add_job():
    return {
        "This will add job description"
    }

@router.get('match-jd')
def match_jon():
    return {
        "This will give projects"
    }