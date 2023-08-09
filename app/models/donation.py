from sqlalchemy import Column, Text, Integer, ForeignKey

from app.core.db import Base


class Donation(Base):
    """Модель пожертвований."""

    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
