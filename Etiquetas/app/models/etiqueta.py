from pydantic import BaseModel
from typing import Optional
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()
# En un proyecto real, importarías tu modelo ORM de SQLAlchemy desde app/db/models.py
from typing import List, Optional





class DBEtiqueta(Base):
    __tablename__ = "etiquetas"

    id = Column(Integer, primary_key=True, index=True)
    precio = Column(Integer)
    nombre = Column(String, index=True)

class EtiquetaBase(BaseModel):
    """
    Propiedades base compartidas por todos los modelos de Etiqueta.
    """
    nombre: str
    precio: Optional[float] = None


class EtiquetaCreate(EtiquetaBase):
    """
    Propiedades requeridas al crear una nueva Etiqueta.
    (Viene en el body de un POST)
    """
    pass  # Hereda de EtiquetaBase


class EtiquetaUpdate(BaseModel):
    """
    Propiedades opcionales al actualizar una Etiqueta.
    (Viene en el body de un PUT o PATCH)
    """
    nombre: Optional[str] = None
    precio: Optional[float] = None


class EtiquetaInDBBase(EtiquetaBase):
    """
    Propiedades de una Etiqueta tal como está almacenada en la base de datos.
    Incluye campos auto-generados como el 'id'.
    """
    id: int

    class Config:
        # Permite que Pydantic lea datos desde un modelo ORM (ej. SQLAlchemy)
        from_attributes = True


class Etiqueta(EtiquetaInDBBase):
    """
    Propiedades que se devuelven al cliente (response body).
    """
    pass
