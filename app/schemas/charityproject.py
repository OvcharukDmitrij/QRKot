from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, root_validator


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        min_anystr_length = 1


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., max_length=100)
    description: str
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):

    @root_validator
    def param_cannot_be_null(cls, values):
        for k, v in values.items():
            if v is None:
                raise ValueError(f'Значение {k} не может быть пустым!')
        return values
