from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = str(Path(__file__).resolve().parent.parent)


class DbSettings(BaseModel):
    url: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"
    echo: bool = True


class Settings(BaseSettings):
    base_dir: str = BASE_DIR

    db: DbSettings = DbSettings()


settings = Settings()
