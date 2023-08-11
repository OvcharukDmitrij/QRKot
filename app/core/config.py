from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'QRKot'
    app_description: str = ('Приложение для благотворительного'
                            ' фонда поддержки котиков')
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = 'admin@example.com'
    first_superuser_password: Optional[str] = '12345'

    class Config:
        env_file = '.env'


settings = Settings()
