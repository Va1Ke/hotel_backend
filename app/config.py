import os
from dotenv import load_dotenv
from pathlib import Path
from app.utils import get_env_value

env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path)


class Settings:
    POSTGRES_USER: str = get_env_value("POSTGRES_USER")
    POSTGRES_PASSWORD: str = get_env_value("POSTGRES_PASSWORD")
    POSTGRES_HOST: str = get_env_value("POSTGRES_HOST")
    POSTGRES_PORT: str = get_env_value("POSTGRES_PORT")
    POSTGRES_DB: str = get_env_value("POSTGRES_DB")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


settings = Settings()
