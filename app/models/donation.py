from sqlalchemy import Column, Text, Integer, ForeignKey

from app.models.base import BaseModel


class Donation(BaseModel):
    """Модель пожертвований."""

    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
