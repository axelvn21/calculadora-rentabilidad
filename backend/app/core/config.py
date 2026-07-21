import sys
from pathlib import Path
from pydantic_settings import BaseSettings


def get_base_dir():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent.parent


BASE_DIR = get_base_dir()


class Settings(BaseSettings):
    DATABASE_URL: str = f"sqlite:///{BASE_DIR}/calculadora.db"
    APP_NAME: str = "Calculadora de Rentabilidad"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = not getattr(sys, 'frozen', False)

    class Config:
        env_file = ".env"


settings = Settings()
