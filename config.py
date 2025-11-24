from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class Settings(BaseSettings):
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg://aiganym:lDVMmlv6rYvsgTVgsD1Ej9HzBQhnVvWV@dpg-d4i4d7umcj7s73ccndv0-a.frankfurt-postgres.render.com/caregivers_db_3eiv?sslmode=require"
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings():
    return Settings()

