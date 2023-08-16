from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.donation import donation_crud
from app.models import User, CharityProject
from app.schemas.donation import DonationBase, DonationCreate, DonationDB
from app.services.investment import calculation

router = APIRouter()


@router.post(
    '/',
    response_model=DonationCreate,
    response_model_exclude_none=True
)
async def create_new_donation(
        donation: DonationBase,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Создание нового пожертвования."""

    new_donation = await donation_crud.create(donation, session, user)
    await calculation(new_donation, CharityProject, session)

    return new_donation


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)
):
    """Получения списка всех пожертвований. Только для суперюзеров."""

    donations = await donation_crud.get_multi(session)

    return donations


@router.get(
    '/{my}',
    response_model=list[DonationCreate],
    response_model_exclude_none=True
)
async def get_donations_by_user(
        my: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
):
    """Получения списка всех пожертвований пользователя.
    Только для зарегистрированного пользователя."""

    donations = await donation_crud.get_donations_by_user(my, session)

    return donations


@router.patch('/{donation_id}')
async def update_donation():
    """Изменение существующего пожертвования запрещено."""

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Запрещено редактировать пожертвования!'
    )


@router.delete('/{donation_id}')
async def remove_donation():
    """Удаление существующего пожертвования запрещено."""

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Запрещено удалять пожертвования!'
    )