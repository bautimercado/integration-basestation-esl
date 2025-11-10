from fastapi import FastAPI
from app.api.v1.api import api_router
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware

# Creación de la instancia de la aplicación FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.1.0",
    openapi_url="/api/v1/openapi.json" # URL para el schema OpenAPI
)

# Configuración de CORS (Cross-Origin Resource Sharing)
# Permite que frontends en diferentes dominios accedan a esta API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción, sé más restrictivo. Ej: ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"], # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"], # Permite todos los headers
)

# Incluir el router principal de la API v1
# Todo lo definido en api_router tendrá el prefijo /api/v1
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    """
    Endpoint raíz para verificar que la aplicación está funcionando.
    """
    return {"status": "OK", "message": f"Welcome to {settings.PROJECT_NAME}"}