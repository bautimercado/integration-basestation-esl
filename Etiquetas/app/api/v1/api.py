from fastapi import APIRouter
from app.api.v1.endpoints import etiquetas

# Este es el router principal para la versión 1 de la API.
api_router = APIRouter()

# Incluir el router de 'items'
# Todas las rutas definidas en 'items.router' tendrán ahora el prefijo '/items'
# y serán etiquetadas como "Items" en la documentación de Swagger.
api_router.include_router(etiquetas.router, prefix="/etiquetas", tags=["etiquetas"])

# Si tuvieras más recursos (ej. "users", "products"), los incluirías aquí:
# from app.api.v1.endpoints import users
# api_router.include_router(users.router, prefix="/users", tags=["Users"])