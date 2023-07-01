from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from fastapi.responses import JSONResponse # esse aqui é obrigatprio passar um content, no método delete não serve
from fastapi import Response

from models import Curso

app = FastAPI()

cursos = {
    1: {
        'titulo': 'Programação para Leigos',
        'aulas' : 112,
        'horas' : 58
    },
    2: {
        'titulo': 'Algoritmos e Lógica de Programação',
        'aulas' : 87,
        'horas' : 67
    }
}

@app.get('/cursos')
async def get_cursos():
    return cursos

@app.get('/cursos/{curso_id}')
async def get_cursos(curso_id : int):  # ele trasforma para o tipo inteiro através do type hint
    # tratando as exceções caso não exista o curso
    try:
        curso = cursos[curso_id]
        return curso
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Curso não encontrado'
        )

@app.post('/cursos', status_code=status.HTTP_201_CREATED)
async def post_curso(curso:Curso):
    next_id: int = len(cursos) + 1
    cursos[next_id] = curso
    del curso.id
    return curso

@app.put('/cursos/{curso_id}')
async def put_curso(curso_id:int, curso:Curso):
    if curso_id in cursos:
        cursos[curso_id] = curso
        del curso.id
        return curso
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Não existe um curso com ID {curso_id}'
        )

@app.delete('/cursos/{curso_id}')
async def delete_curso(curso_id: int):
    if curso_id in cursos:
        del cursos[curso_id]
        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Não existe um curso com ID {curso_id}'
        )
    

if __name__ == '__main__':
    import uvicorn
    
    uvicorn.run(
        'main:app',
        host='127.0.0.1',
        port=8000,
        reload=True,
        debug=True
        
    )