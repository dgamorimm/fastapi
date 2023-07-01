from typing import Optional
from pydantic import BaseModel

class Curso(BaseModel):
    id:     Optional[int] = None  # isso faz com que seja opcional
    titulo: str
    aulas:  int
    horas:  int