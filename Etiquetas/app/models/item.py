from pydantic import BaseModel
from typing import Optional

# Este archivo define los "schemas" de Pydantic.
# Estos modelos validan los datos de entrada (request body)
# y formatean los datos de salida (response body).

class ItemBase(BaseModel):
    """
    Propiedades base compartidas por todos los modelos de Item.
    """
    title: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    """
    Propiedades requeridas al crear un nuevo Item.
    (Viene en el body de un POST)
    """
    pass # Hereda title y description

class ItemUpdate(BaseModel):
    """
    Propiedades opcionales al actualizar un Item.
    (Viene en el body de un PUT o PATCH)
    """
    title: Optional[str] = None
    description: Optional[str] = None

class ItemInDBBase(ItemBase):
    """
    Propiedades de un Item tal como está almacenado en la DB.
    Incluye campos auto-generados como el 'id'.
    """
    id: int

    class Config:
        # Permite que Pydantic lea el modelo desde un objeto ORM (ej. SQLAlchemy)
        # ej: Item.model_validate(db_item)
        from_attributes = True

class Item(ItemInDBBase):
    """
    Propiedades que se devuelven al cliente (en la respuesta de la API).
    """
    pass