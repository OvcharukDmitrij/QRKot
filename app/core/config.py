from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'QRKot'
    app_description: str = ('Приложение для благотворительного'
                            ' фонда поддержки котиков')
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'


    class Config:
        env_file = '.env'


settings = Settings()