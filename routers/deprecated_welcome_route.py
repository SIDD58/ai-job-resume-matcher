from fastapi import APIRouter

router = APIRouter()

@router.get('/{user}')
def welcome(user:str,nick_name:str | None=None)->dict[str,str|int|None]:
    return {
        'User': user,
        'Nick name':nick_name
    }

@router.get('/')
def api_status():
    return {
        "It is working"
    }