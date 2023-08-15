from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_name_duplicate, check_charityproject_exists)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charityproject_crud
from app.schemas import (
    CharityProjectUpdate, CharityProjectCreate, CharityProjectDB
)
from app.services.investment import calculation_in_new_project

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_new_charityproject(
        charityproject: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Создание нового проекта. Только для суперюзеров."""

    await check_name_duplicate(charityproject.name, session)
    new_project = await charityproject_crud.create(charityproject, session)
    # new_project = await calculation_in_new_project(charityproject, session)

    return new_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_charityprojects(
        session: AsyncSession = Depends(get_async_session),
):
    """Получение списка всех проектов."""

    all_charityprojects = await charityproject_crud.get_multi(session)

    return all_charityprojects


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_charityproject(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Изменение существующего проекта. Только для суперюзеров."""

    db_project = await check_charityproject_exists(project_id, session)

    if db_project.fully_invested:
        raise HTTPException(
            status_code=400,
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


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def remove_charityproject(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """Удаление проекта. Только для суперюзеров."""

    project = await check_charityproject_exists(project_id, session)

    if project.invested_amount:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )

    project = await charityproject_crud.remove(project, session)

    return project
