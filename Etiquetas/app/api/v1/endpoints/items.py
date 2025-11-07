from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

# Importar dependencias, modelos y servicios
from app.db.session import get_db
from app.models.item import Item, ItemCreate, ItemUpdate
from app.services.item_service import item_service

# Crear un nuevo router para los endpoints de items
router = APIRouter()

@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(
    item: ItemCreate,
    db: AsyncSession = Depends(get_db) # Inyectar la sesión de DB
):
    """
    Crea un nuevo item.
    
    La lógica de creación está en `item_service`.
    `response_model=Item` asegura que la respuesta tenga el formato del schema `Item`.
    """
    return await item_service.create_item(db=db, item=item)

@router.get("/", response_model=List[Item])
async def read_items(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    Obtiene una lista de items.
    
    Acepta parámetros de paginación `skip` y `limit`.
    `response_model=List[Item]` asegura que la respuesta sea una lista de `Item`.
    """
    items = await item_service.get_items(db=db)
    return items[skip : skip + limit]

@router.get("/{item_id}", response_model=Item)
async def read_item(
    item_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Obtiene un item específico por su ID.
    """
    db_item = await item_service.get_item(db=db, item_id=item_id)
    if db_item is None:
        # Si el item no se encuentra, devuelve un error 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return db_item