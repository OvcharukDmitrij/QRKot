from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_name_duplicate, check_charityproject_exists)
from app.core.db import get_async_session
from app.crud.charityproject import charityproject_crud
from app.schemas.charityproject import (
    CharityProjectUpdate, CharityProjectCreate)
from app.services.investment import invest_in_new_project

router = APIRouter()


@router.post('/')
async def create_new_charityproject(
        charityproject: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Создание нового проекта."""

    await check_name_duplicate(charityproject.name, session)
    new_project = await invest_in_new_project(charityproject, session)
    new_project = await charityproject_crud.create(new_project, session)

    return new_project


@router.get('/')
async def get_all_charityprojects(
        session: AsyncSession = Depends(get_async_session),
):
    """Получение списка всех проектов."""

    all_charityprojects = await charityproject_crud.get_multi(session)

    return all_charityprojects


@router.patch('/{project_id}')
async def partially_update_charityproject(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Изменение существующего проекта."""

    db_project = await check_charityproject_exists(project_id, session)

    if db_project.fully_invested:
        raise HTTPException(
            status_code=422,
            detail='Закрытый проект нельзя редактировать!'
        )

    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    if obj_in.full_amount is not None:
        if obj_in.full_amount < db_project.invested_amount:
            raise HTTPException(
                status_code=422,
                detail='Нельзя установить требуемую'
                       ' сумму меньше уже вложенной!'
            )

    project = await charityproject_crud.update(db_project, obj_in, session)

    return project


@router.delete('/{project_id}')
async def remove_charityproject(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """Удаление проекта."""

    project = await check_charityproject_exists(project_id, session)

    if project.invested_amount:
        raise HTTPException(
            status_code=422,
            detail='Нельзя удалить проект, в который уже были'
                   'инвестированы средства, его можно только закрыть.'
        )

    project = await charityproject_crud.remove(project, session)

    return project
