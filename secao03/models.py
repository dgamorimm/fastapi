from typing import Optional
from pydantic import BaseModel, validator

class Curso(BaseModel):
    id:     Optional[int] = None  # isso faz com que seja opcional
    titulo: str
    aulas:  int
    horas:  int
    
    @validator('titulo')
    def validar_titulo(cls, value : str):
        # Validacao 1
        palavras = value.split(' ')
        if len(palavras) < 3:
            raise ValueError('O título deve ter pelo menos 3 palavras')
        # Validacao 2
        if value.islower():
            raise ValueError('O título deve ser capitalizado')
        
        return value

cursos = [
    Curso(id=1, titulo='Programação para Leigos', aulas=42, horas=56),
    Curso(id=2, titulo='Programação com Javascript', aulas=38, horas=99),
    Curso(id=3, titulo='Programação Front com React', aulas=71, horas=22),
    Curso(id=4, titulo='React Native Patterns', aulas=89, horas=120),
]