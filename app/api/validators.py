from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import charityproject_crud
from app.models import CharityProject


async def check_charityproject_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """Проверка наличия проекта в БД и получение его по id."""

    project = await charityproject_crud.get(
        project_id, session
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )

    return project


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    """Проверка уникальности имени проекта."""

    project_id = await charityproject_crud.get_project_id_by_name(
        project_name, session
    )

    if project_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Проект с таким именем уже существует!',
        )
