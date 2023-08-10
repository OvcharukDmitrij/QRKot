from fastapi import APIRouter, HTTPException, Depends

from app.crud.charityproject import create_charityproject, get_project_id_by_name, read_all_charityprojects_from_db
from app.schemas.charityproject import CharityProjectCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_async_session

router = APIRouter(
    prefix='/charity_project',
    tags=['Charity project'])


@router.post('/')
async def create_new_charityproject(
        charityproject: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    project_id = await get_project_id_by_name(charityproject.name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Проект с таким именем уже существует!'
        )
    new_project = await create_charityproject(charityproject, session)
    return new_project


@router.get('/')
async def get_all_charityprojects(
        session: AsyncSession = Depends(get_async_session),
):
    all_charityprojects = await read_all_charityprojects_from_db(session)
    return all_charityprojects
