from symtable import Class

from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    postgres_user: str
    postgres_password: str
    postgres_db: str
    host: str
    port: int


    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
print(settings.database_url)