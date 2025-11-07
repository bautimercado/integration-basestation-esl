from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from typing import AsyncGenerator

# Crear el "engine" de base de datos asíncrono
# Este es el punto de conexión principal a la DB.
async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True, # Log de las consultas SQL (útil en desarrollo)
)

# Crear una fábrica de sesiones asíncronas
# Esta fábrica creará nuevas sesiones (AsyncSession) cuando se la llame.
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False, # Evita que los objetos se expiren después de un commit
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependencia de FastAPI para obtener una sesión de base de datos.
    
    Esto es un generador que:
    1. Crea una nueva sesión de DB (`AsyncSessionLocal()`).
    2. La provee (yield) a la ruta que la depende.
    3. Atrapa cualquier error, hace rollback si es necesario.
    4. Cierra la sesión al finalizar (en el finally).
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()