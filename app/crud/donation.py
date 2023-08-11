from app.schemas.donation import DonationBase, DonationDB
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.donation import Donation


async def create_donation(
        new_donation: DonationBase,
        session: AsyncSession,
) -> Donation:
    new_donation_data = new_donation.dict()
    new_donation_db = Donation(**new_donation_data)

    session.add(new_donation_db)
    await session.commit()
    await session.refresh(new_donation_db)

    return new_donation_db