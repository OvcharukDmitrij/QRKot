from sqlalchemy import Column, Text, Integer, ForeignKey

from app.core.db import Base
from app.models.base import BaseModel


class Donation(Base, BaseModel):
    """Модель пожертвований."""

    # user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
