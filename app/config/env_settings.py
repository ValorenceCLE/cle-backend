from pydantic_settings import BaseSettings
from pathlib import Path

class EnvSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    USER_USERNAME: str
    USER_PASSWORD_HASH: str

    ADMIN_USERNAME: str
    ADMIN_PASSWORD_HASH: str

    class Config:
        env_file = Path(__file__).parent.parent / "app.env"
        env_file_encoding = "utf-8"

env = EnvSettings()
