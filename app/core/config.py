from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'QRKot'
    app_description: str = ('Приложение для благотворительного'
                            ' фонда поддержки котиков')
    database_url: str = 'sqlite+aiosqlite:///./fastapi_qrkot.db'
    secret: str = 'SECRET'
    lifetime_seconds: int = 3600
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
