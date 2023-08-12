from sqlalchemy import select

from app.schemas.charityproject import CharityProjectCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Donation
from datetime import datetime


async def invest_in_new_project(
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
            donation.invested_amount += free_money
            donation.fully_invested = True
            donation.close_date = datetime.now()
        else:
            project['invested_amount'] += money_is_required
            project['close_date'] = datetime.now()
            project['fully_invested'] = True
            donation.invested_amount += money_is_required
            break

    return project