from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt


class DonationBase(BaseModel):
    """Базовая схема."""

    full_amount: PositiveInt
    comment: Optional[str]


class DonationCreate(DonationBase):
    """Схема для возврата данных при создании пожертвования."""

    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDB(DonationBase):
    """Схема для возврата данных при просмотре всех пожертвования."""

    id: int
    create_date: datetime
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
