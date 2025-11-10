from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

# Importar dependencias, modelos y servicios
from app.db.session import get_db
from app.models.etiqueta import Etiqueta, EtiquetaCreate,EtiquetaUpdate
from app.services.etiqueta_service import Etiqueta_service

# Crear un nuevo router para los endpoints de Etiquetas
router = APIRouter()

@router.post("/", response_model=Etiqueta, status_code=status.HTTP_201_CREATED)
async def create_etiqueta(
    Etiqueta: EtiquetaCreate,
    db: AsyncSession = Depends(get_db) # Inyectar la sesión de DB
):
    """
    Crea un nuevo Etiqueta.
    
    La lógica de creación está en `Etiqueta_service`.
    `response_model=Etiqueta` asegura que la respuesta tenga el formato del schema `Etiqueta`.
    """
    return await Etiqueta_service.create_etiqueta(db=db, Etiqueta=Etiqueta)

@router.get("/", response_model=List[Etiqueta])
async def read_etiquetas(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    Obtiene una lista de Etiquetas.
    
    Acepta parámetros de paginación `skip` y `limit`.
    `response_model=List[Etiqueta]` asegura que la respuesta sea una lista de `Etiqueta`.
    """
    Etiquetas = await Etiqueta_service.get_etiquetas(db=db)
    return Etiquetas[skip : skip + limit]

@router.get("/{id}", response_model=Etiqueta)
async def read_etiqueta(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Obtiene un Etiqueta específico por su ID.
    """
    db_Etiqueta = await Etiqueta_service.get_etiqueta(db=db, id=id)
    if db_Etiqueta is None:
        # Si el Etiqueta no se encuentra, devuelve un error 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Etiqueta not found")
    return db_Etiqueta