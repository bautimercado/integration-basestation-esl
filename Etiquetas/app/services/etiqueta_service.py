from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.etiqueta import EtiquetaCreate, EtiquetaUpdate, DBEtiqueta
from typing import List, Optional




class EtiquetaService:
    """
    Clase de servicio para manejar la lógica de negocio de los Items.
    Mantiene la lógica fuera de las rutas de la API.
    """

    async def get_etiquetas(self, db: AsyncSession) -> List[DBEtiqueta]:
        """
        Obtiene todos los items.
        """
        result = await db.execute(select(DBEtiqueta))
        return result.scalars().all()




    async def create_etiqueta(self, db: AsyncSession, Etiqueta: EtiquetaCreate) -> DBEtiqueta:
        """
        Crea un nuevo item.
        """
        global next_id
        # --- Lógica real de SQLAlchemy (comentada) ---
        db_item = DBEtiqueta(**Etiqueta.model_dump())
        db.add(db_item)
        await db.commit()
        await db.refresh(db_item)
        return db_item


    async def get_etiqueta(self, db: AsyncSession, id: int) -> Optional[DBEtiqueta]:
        """
        Obtiene un item por su ID.
        """

        result = await db.execute(select(DBEtiqueta).filter(DBEtiqueta.id == id))
        return result.scalars().first()



# Instancia única del servicio para ser usada en la API
Etiqueta_service = EtiquetaService()