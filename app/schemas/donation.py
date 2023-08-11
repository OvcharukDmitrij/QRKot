from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt


class DonationBase(BaseModel):
    """Базовая схема."""

    full_amount: PositiveInt
    comment: Optional[str]


class DonationDB(DonationBase):
    """Схема для возврата данных при создании пожертвования
    и получения списка всех пожертвований пользователя."""

    id: int
    create_date: datetime

    class Config:
        orm_mode = True
