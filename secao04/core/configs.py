# configurações gerais que vamos usar em todo o projeto

from os import getenv
from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """
        Configurações gerais usadas na aplicação
    """
    API_V1_STR:str = '/api/v1'
    DB_URL:str = f'postgresql+asyncpg://{getenv("PGSQL_USERNAME")}:{getenv("PGSQL_PASSWORD")}@localhost:5432/faculdade'
    DBBaseModel = declarative_base()
    
    class Config:
        case_sensitive = True
        
settings = Settings()