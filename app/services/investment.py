from operator import itemgetter
from typing import Union

from sqlalchemy import select

from app.schemas.charity_project import CharityProjectCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Donation, CharityProject
from datetime import datetime


async def calculation_in_new_project(
        data,
        session: AsyncSession
):
    project = data.dict()
    open_donations = await session.execute(select(Donation).where(
        Donation.fully_invested == 0
    ))
    open_donations = open_donations.scalars().all()
    project['invested_amount'] = 0
    for donation in open_donations:
        free_money = donation.full_amount - donation.invested_amount
        money_is_required = project['full_amount'] - project['invested_amount']
        if free_money < money_is_required:
            project['invested_amount'] += free_money
            donation.invested_amount = donation.full_amount
            donation.fully_invested = True
            donation.close_date = datetime.now()
        elif free_money > money_is_required:
            project['invested_amount'] += money_is_required
            project['close_date'] = datetime.now()
            project['fully_invested'] = True
            donation.invested_amount += money_is_required
            break
        else:
            project['invested_amount'] = money_is_required
            donation.invested_amount += money_is_required
            donation.fully_invested = project['fully_invested'] = True
            donation.close_date = project['close_date'] = datetime.now()

    return project


async def calculation_in_new_donation(
        data,
        session: AsyncSession
):
    donation = data.dict()
    open_projects = await session.execute(select(CharityProject).where(
        CharityProject.fully_invested == 0
    ))
    open_projects = open_projects.scalars().all()
    donation['invested_amount'] = 0
    for project in open_projects:
        free_money = donation['full_amount'] - donation['invested_amount']
        money_is_required = project.full_amount - project.invested_amount
        if free_money < money_is_required:
            project.invested_amount += free_money
            donation['invested_amount'] = donation['full_amount']
            donation['fully_invested'] = True
            donation['close_date'] = datetime.now()
            break
        elif free_money > money_is_required:
            project.invested_amount += money_is_required
            project.close_date = datetime.now()
            project.fully_invested = True
            donation['invested_amount'] = money_is_required
        else:
            project.invested_amount += money_is_required
            donation['invested_amount'] = money_is_required
            donation['fully_invested'] = project.fully_invested = True
            donation['close_date'] = project.close_date = datetime.now()

    return donation


# async def calculation(
#         data,
#         model: Union[CharityProject, Donation],
#         session: AsyncSession
# ):
#     resourсe = data.dict()
#     open_objects = await session.execute(select(model).where(
#         model.fully_invested == 0
#     )
#     )
#     open_objects = open_objects.scalars().all()
#
#     resourсe['invested_amount'] = 0
#
#     for object in open_objects:
#
#         if model == CharityProject:
#             free_money = object.full_amount - object.invested_amount
#             money_is_required = resourсe['full_amount'] - resourсe['invested_amount']
#         else:
#             free_money = resourсe['full_amount'] - resourсe['invested_amount']
#             money_is_required = object.full_amount - object.invested_amount
#
#         if free_money < money_is_required:
