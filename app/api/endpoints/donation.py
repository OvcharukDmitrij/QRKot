from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationBase, DonationDB

router = APIRouter()


@router.post('/', response_model=DonationDB)
async def create_new_donation(
        donation: DonationBase,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Создание нового пожертвования."""

    new_donation = await donation_crud.create(donation, session, user)

    return new_donation


@router.get('/')
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)
):
    """Получения списка всех пожертвований."""

    donations = await donation_crud.get_multi(session)

    return donations


@router.get('/{my}', response_model=list[DonationDB])
async def get_donations_by_user(
        my: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Получения списка всех пожертвований пользователя."""

    donations = await donation_crud.get_donations_by_user(my, session)

    return donations
