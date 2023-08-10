from fastapi import APIRouter, HTTPException

from app.crud.charityproject import create_charityproject, get_project_id_by_name
from app.schemas.charityproject import CharityProjectCreate

router = APIRouter()


@router.post('/charity_project/')
async def create_new_charityproject(
        charityproject: CharityProjectCreate,
):
    project_id = await get_project_id_by_name(charityproject.name)
    if project_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Проект с таким именем уже существует!'
        )
    new_project = await create_charityproject(charityproject)
    return new_project
