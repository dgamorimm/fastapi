from pydantic import BaseSettings
from os import getenv
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    API_V1_STR:str = '/api/v1'
    DB_URL:str = f'postgresql+asyncpg://{getenv("PGSQL_USERNAME")}:{getenv("PGSQL_PASSWORD")}@localhost:5432/faculdade'
    
    class Config:
        case_sensitive = True

settings:Settings = Settings()