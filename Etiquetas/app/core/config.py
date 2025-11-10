from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Configuración de la aplicación, cargada desde variables de entorno
    o un archivo .env.
    """
    
    # URL de la base de datos. 
    # Ejemplo para PostgreSQL asíncrono: "postgresql+asyncpg://user:password@localhost/dbname"
    # Usamos un valor default para que la app corra sin .env (con el servicio mock)
    DATABASE_URL: str = "mysql+aiomysql://root:root@localhost:3306/etiquetas"
    PROJECT_NAME: str = "FastAPI Backend Boilerplate"

    class Config:
        # Nombre del archivo del cual cargar las variables
        env_file = ".env"
        env_file_encoding = "utf-8"

# Instancia única de la configuración
settings = Settings()