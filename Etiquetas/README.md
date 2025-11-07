Estructura de Backend con FastAPI

Este proyecto demuestra una estructura escalable y basada en buenas prácticas para construir un backend con FastAPI.

Estructura de Directorios

.
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── api.py           # Agregador de routers v1
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           └── items.py     # Endpoints para /items
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py        # Configuración (variables de entorno)
│   ├── db/
│   │   ├── __init__.py
│   │   └── session.py       # Sesión de DB y dependencia get_db
│   ├── models/
│   │   ├── __init__.py
│   │   └── item.py          # Modelos Pydantic (schemas)
│   └── services/
│       ├── __init__.py
│       └── item_service.py  # Lógica de negocio (business logic)
├── .env                       # Archivo de variables de entorno (NO subir a git)
├── main.py                    # Punto de entrada de la aplicación
├── requirements.txt           # Dependencias de Python
└── README.md


Puntos Clave

Separación de Capas:

main.py: Punto de entrada y configuración global (CORS, middlewares).

app/api/: Capa de API (HTTP). Maneja peticiones, valida datos de entrada/salida y llama a los servicios.

app/services/: Capa de Lógica de Negocio. Contiene la lógica real de la aplicación.

app/models/: Capa de Datos (Schemas). Define la forma de los datos (Pydantic).

app/db/: Capa de Acceso a Datos. Gestiona la conexión y sesión con la base de datos.

Inyección de Dependencias:

La función get_db en app/db/session.py es un generador que provee una sesión de base de datos a las rutas que la necesiten, usando Depends(get_db).

Configuración Centralizada:

app/core/config.py usa pydantic-settings para cargar la configuración desde variables de entorno (y un archivo .env), haciéndolo fácil de gestionar en diferentes entornos (dev, staging, prod).

Routers Modulares:

APIRouter se usa en app/api/v1/endpoints/ para agrupar endpoints relacionados.

app/api/v1/api.py los combina todos, y main.py incluye ese router principal. Esto mantiene main.py limpio.

Modelos Pydantic Explícitos:

Se usan diferentes modelos para diferentes operaciones (ItemCreate, ItemUpdate, Item) para una validación de datos estricta y clara.

Cómo Ejecutar

Crear un entorno virtual:

python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate


Instalar dependencias:

pip install -r requirements.txt


Crear archivo .env (Opcional, para DB real):
Crea un archivo .env en la raíz con tu URL de base de datos:

DATABASE_URL="postgresql+asyncpg://tu_usuario:tu_pass@localhost/tu_db"


(El código actual usa un servicio simulado, por lo que este paso no es estrictamente necesario para ejecutarlo, pero es la práctica correcta).

Ejecutar el servidor:

uvicorn main:app --reload


Acceder a la documentación:
Visita http://127.0.0.1:8000/docs para ver la interfaz de Swagger UI.