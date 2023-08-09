from sqlalchemy import Column, Integer, Boolean, DateTime


class BaseModel:
    full_amount = Column(Integer)
    invested_amount = Column(Integer)
    fully_invested = Column(Boolean)
    create_date = Column(DateTime)
    close_date = Column(DateTime)
