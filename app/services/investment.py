from datetime import datetime
from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def close_object(*args):
    objects = []
    for object in args:
        object.close_date = datetime.now()
        object.fully_invested = True
        object.invested_amount = object.full_amount
        objects.append(object)
    return objects


async def calculation(
        new_obj_db: Union[CharityProject, Donation],
        model: Union[CharityProject, Donation],
        session: AsyncSession
) -> None:
    open_resources = await session.execute(select(model).where(
        model.fully_invested == 0
    ))

    if open_resources:
        for resource in open_resources.scalars().all():
            free_money = resource.full_amount - resource.invested_amount
            money_is_required = (
                new_obj_db.full_amount - new_obj_db.invested_amount
            )

            if free_money < money_is_required:
                new_obj_db.invested_amount += free_money
                await close_object(resource)

            elif free_money > money_is_required:
                resource.invested_amount += money_is_required
                await close_object(new_obj_db)
                break

            else:
                new_obj_db, resource = await close_object(new_obj_db, resource)

            session.add(resource)
            session.add(new_obj_db)

        await session.commit()
        await session.refresh(new_obj_db)
