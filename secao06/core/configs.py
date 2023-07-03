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
    
    """
        essa é uma lib built in do python e
        vai servir para gerar o JWT_SECRET
        
        import secrets
        
        token: str = secrets.token_urlsafe(32)
    """
    JWT_SECRET:str =  getenv('JWT_SECRET')
    ALGORITHM:str = 'HS256'
    # 60 minutos * 24 horas * 7 dias => 1 Semana
    ACCESS_TOKEN_EXPIRE_MINUTES:int = 60 * 24 * 7
    
    class Config:
        case_sensitive = True

settings = Settings()