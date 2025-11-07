from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.item import ItemCreate, ItemUpdate
# En un proyecto real, importarías tu modelo ORM de SQLAlchemy desde app/db/models.py
# from app.db.models import Item as DBItem
from typing import List, Optional

# --- INICIO: SIMULACIÓN DE DB ---
# En un proyecto real, esta clase DBItem estaría en `app/db/models.py`
# y heredaría de `Base` (declarative_base() de SQLAlchemy).
class DBItem:
    def __init__(self, id, title, description):
        self.id = id
        self.title = title
        self.description = description

# Usamos un diccionario en memoria para simular la base de datos
MOCK_DB_ITEMS = {
    1: DBItem(id=1, title="Item 1 (Mock)", description="Descripción 1"),
    2: DBItem(id=2, title="Item 2 (Mock)", description="Descripción 2"),
}
next_id = 3
# --- FIN: SIMULACIÓN DE DB ---


class ItemService:
    """
    Clase de servicio para manejar la lógica de negocio de los Items.
    Mantiene la lógica fuera de las rutas de la API.
    """

    async def get_items(self, db: AsyncSession) -> List[DBItem]:
        """
        Obtiene todos los items.
        """
        # --- Lógica real de SQLAlchemy (comentada) ---
        # result = await db.execute(select(DBItem))
        # return result.scalars().all()
        # --- Fin Lógica real ---
        
        # Lógica simulada
        return list(MOCK_DB_ITEMS.values())

    async def create_item(self, db: AsyncSession, item: ItemCreate) -> DBItem:
        """
        Crea un nuevo item.
        """
        global next_id
        # --- Lógica real de SQLAlchemy (comentada) ---
        # db_item = DBItem(**item.model_dump())
        # db.add(db_item)
        # await db.commit()
        # await db.refresh(db_item)
        # return db_item
        # --- Fin Lógica real ---

        # Lógica simulada
        new_db_item = DBItem(id=next_id, **item.model_dump())
        MOCK_DB_ITEMS[next_id] = new_db_item
        next_id += 1
        return new_db_item

    async def get_item(self, db: AsyncSession, item_id: int) -> Optional[DBItem]:
        """
        Obtiene un item por su ID.
        """
        # --- Lógica real de SQLAlchemy (comentada) ---
        # result = await db.execute(select(DBItem).filter(DBItem.id == item_id))
        # return result.scalars().first()
        # --- Fin Lógica real ---

        # Lógica simulada
        return MOCK_DB_ITEMS.get(item_id)

# Instancia única del servicio para ser usada en la API
item_service = ItemService()