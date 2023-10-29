from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = str(Path(__file__).resolve().parent.parent)


class Setting(BaseSettings):
    base_dir: str = BASE_DIR
    db_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"
    db_echo: bool = True


setting = Setting()
