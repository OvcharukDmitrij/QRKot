from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charityproject import create_charityproject, \
    get_project_id_by_name, read_all_charityprojects_from_db, \
    get_project_by_id, update_charityproject, delete_charityproject
from app.models import CharityProject
from app.schemas.charityproject import CharityProjectUpdate, \
    CharityProjectCreate

router = APIRouter()


@router.post('/')
async def create_new_charityproject(
        charityproject: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Создание нового проекта."""

    await check_name_duplicate(charityproject.name, session)
    new_project = await create_charityproject(charityproject, session)

    return new_project


@router.get('/')
async def get_all_charityprojects(
        session: AsyncSession = Depends(get_async_session),
):
    """Получение списка всех проектов."""

    all_charityprojects = await read_all_charityprojects_from_db(session)

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

    project = await update_charityproject(db_project, obj_in, session)

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

    project = await delete_charityproject(project, session)

    return project


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    """Проверка уникальности имени проекта."""

    project_id = await get_project_id_by_name(project_name, session)

    if project_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Проект с таким именем уже существует!',
        )


async def check_charityproject_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """Проверка наличия проекта в БД и получение его по id."""

    project = await get_project_by_id(
        project_id, session
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )

    return project
