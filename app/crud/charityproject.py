from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charityproject import CharityProject
from app.schemas.charityproject import CharityProjectUpdate, \
    CharityProjectCreate
from app.crud.base import CRUDBase


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        """Получение id проекта по его имени."""

        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        db_project_id = db_project_id.scalars().first()

        return db_project_id


charityproject_crud = CRUDCharityProject(CharityProject)


#
# async def create_charityproject(
#         new_project: CharityProjectCreate,
#         session: AsyncSession,
# ) -> CharityProject:
#     """Создание нового проекта."""
#
#     new_project_data = new_project.dict()
#     new_project_db = CharityProject(**new_project_data)
#
#     session.add(new_project_db)
#     await session.commit()
#     await session.refresh(new_project_db)
#
#     return new_project_db
#
#
# async def update_charityproject(
#         db_project: CharityProject,
#         project_in: CharityProjectUpdate,
#         session: AsyncSession,
# ) -> CharityProject:
#     """Изменение существующего проекта."""
#
#     obj_data = jsonable_encoder(db_project)
#     update_data = project_in.dict(exclude_unset=True)
#
#     for field in obj_data:
#         if field in update_data:
#             setattr(db_project, field, update_data[field])
#
#     session.add(db_project)
#     await session.commit()
#     await session.refresh(db_project)
#
#     return db_project
#
#
# async def delete_charityproject(
#         db_project: CharityProject,
#         session: AsyncSession,
# ) -> CharityProject:
#     """Удаление проекта."""
#
#     await session.delete(db_project)
#     await session.commit()
#
#     return db_project
#
#
# async def read_all_charityprojects_from_db(
#         session: AsyncSession,
# ) -> list[CharityProject]:
#     """Получение списка всех проектов."""
#
#     db_projects = await session.execute(select(CharityProject))
#
    #     return db_projects.scalars().all()





