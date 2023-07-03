from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models.curso_model import CursoModel
from core.deps import get_session

# Bypass qarning SQLModel select
# desabilitando os warnings do sqlmodel
from sqlmodel.sql.expression import Select, SelectOfScalar
SelectOfScalar.inherit_cache = True  #type: ignore
Select.inherit_cache = True  # type: ignore
# Fim Bypass

router = APIRouter()

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=CursoModel)
async def post_curso(curso:CursoModel, db:AsyncSession = Depends(get_session)):
    novo_curso = CursoModel(
        titulo=curso.titulo,
        aulas=curso.aulas,
        horas=curso.horas
    )
    db.add(novo_curso)
    await db.commit()
    
    return novo_curso

@router.get('/', response_model=List[CursoModel])
async def get_cursos(db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel)
        result = await session.execute(query)
        cursos:List[CursoModel] = result.scalars().all()
        
        return cursos

@router.get('/{curso_id}', response_model=CursoModel, status_code=status.HTTP_200_OK)
async def get_curso(curso_id:int, db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso:CursoModel = result.scalar_one_or_none()
        
        if not curso:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Curso {curso_id} não encontrado')
        
        return curso

@router.put('/{curso_id}', response_model=CursoModel, status_code=status.HTTP_202_ACCEPTED)
async def put_curso(curso_id:int, curso:CursoModel, db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso_up:CursoModel = result.scalar_one_or_none()
        
        if not curso_up:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Curso {curso_id} não encontrado')
        else:
            curso_up.titulo = curso.titulo
            curso_up.aulas = curso.aulas
            curso_up.horas = curso.horas
            
            await session.commit()
            return curso_up
        
@router.delete('/{curso_id}', status_code=status.HTTP_204_NO_CONTENT)
async def put_curso(curso_id:int, db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso_del:CursoModel = result.scalar_one_or_none()
        
        if not curso_del:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Curso {curso_id} não encontrado')
        else:
            await session.delete(curso_del)
            await session.commit()
            # Colocamos por conta de um bug no FastAPI
            return Response(status_code=status.HTTP_204_NO_CONTENT)