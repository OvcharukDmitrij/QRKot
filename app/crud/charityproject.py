from typing import Optional

from sqlalchemy import select

from app.core.db import AsyncSessionLocal
from app.models.charityproject import CharityProject
from app.schemas.charityproject import CharityProjectCreate


async def create_charityproject(
        new_project: CharityProjectCreate
) -> CharityProject:
    """Создание нового проекта."""

    new_project_data = new_project.dict()
    new_project_db = CharityProject(**new_project_data)

    async with AsyncSessionLocal() as session:
        session.add(new_project_db)
        await session.commit()
        await session.refresh(new_project_db)

    return new_project_db


async def get_project_id_by_name(project_name: str) -> Optional[int]:
    """Проверка наличия проекта с указанным именем."""

    async with AsyncSessionLocal() as session:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        db_project_id = db_project_id.scalars().first()
    return db_project_id
