from typing import List, Dict, Any, Optional

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from fastapi.responses import JSONResponse # esse aqui é obrigatprio passar um content, no método delete não serve
from fastapi import Response
from fastapi import Path  # serve para ajustar a doc e colocar validadores
from fastapi import Query
from fastapi import Header
from fastapi import Depends

from time import sleep

from models import Curso
from models import cursos

def fake_db():
    try:
        print('Abrindo conexão com banco de dados')
        sleep(1)
    finally:
        print('Fechando conexão com banco de dados')
        sleep(1)

# adiciona o titula na documentação
# adiciona a versão na documentação
app = FastAPI(
    title='API de cursos da Geek University',
    version='0.0.1',
    description='Uma API para estudo do FastAPI'
)

# description e summary serve para a documentação
# response_model também serve para colocar o que vai retornar na documentação
# response_description retorna a mensagem de sucesso
@app.get('/cursos', 
         description='Retorna todos os cursos ou uma lista vazia', 
         summary='Retorna todos os cursos',
         response_model=List[Curso],
         response_description='Cursos encontrados com sucesso')
async def get_cursos(db:Any = Depends(fake_db)):
    return cursos

@app.get('/cursos/{curso_id}',
         description='Retorna um curso em um dicionário', 
         summary='Retorna um único curso',
         response_model=Curso)
async def get_cursos(curso_id : int = Path(title='ID do curso',description='Deve ser entre 1 e 4',gt=0,lt=5), db:Any = Depends(fake_db)):  # ele trasforma para o tipo inteiro através do type hint
    # tratando as exceções caso não exista o curso
    try:
        curso = cursos[curso_id - 1]
        return curso
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Curso não encontrado'
        )

@app.post('/cursos', 
          status_code=status.HTTP_201_CREATED,
          response_model=Curso)
async def post_curso(curso:Curso, db:Any = Depends(fake_db)):
    next_id: int = len(cursos) + 1
    curso.id = next_id
    cursos.append(curso)
    return curso

@app.put('/cursos/{curso_id}')
async def put_curso(curso_id:int, curso:Curso, db:Any = Depends(fake_db)):
    if curso_id in cursos:
        cursos[curso_id - 1] = curso
        del curso.id
        return curso
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Não existe um curso com ID {curso_id}'
        )

@app.delete('/cursos/{curso_id}')
async def delete_curso(curso_id:int, db:Any = Depends(fake_db)):
    if curso_id in cursos:
        del cursos[curso_id - 1]
        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Não existe um curso com ID {curso_id}'
        )

@app.get('/calculadora')
async def calcular(a:int = Query(gt=5), b:int = Query(gt=10), c:Optional[int] = None, x_geek: str = Header()):
    # deixa o c como opcional
    soma: int = a + b
    if c:
        soma += c
    print(f'X-GEEK: {x_geek}')
    return {'resultado': soma}

if __name__ == '__main__':
    import uvicorn
    
    uvicorn.run(
        'main:app',
        host='127.0.0.1',
        port=8000,
        reload=True,
        use_colors=True
    )