from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.donation import create_donation
from app.schemas.donation import DonationBase, DonationDB
from app.models import User
from app.core.user import current_user, current_superuser


router = APIRouter()


@router.post('/', response_model=DonationDB)
async def create_new_donation(
        donation: DonationBase,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Создание нового пожертвования."""

    new_donation = await create_donation(donation, session, user)

    return new_donation
