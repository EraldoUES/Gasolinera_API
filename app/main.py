from fastapi import FastAPI

#Importar routers de cada entidad
from app.routes.rol_routes import rol_router
from app.routes.tipo_combustible_routes import tipo_combustible_router
from app.routes.user_routes import user
from app.routes.user_routes_2 import user2
from app.routes.vehiculos_routes import vehiculos_router
from app.routes.vehiculos_routes_2 import vehiculos_router2
from app.routes.gasolineras_routes import gasolineras_router
from app.routes.proyecto_routes import proyecto_router
from app.routes.bitacora_routes import bitacora_router
from app.routes.bitacora_routes_2 import bitacora_router2
from app.routes.log_routes import log_router

#Instancia de la aplicación FastAPI
app = FastAPI(
    title="Gestion Combustible API",
    description="API para gestionar la base de datos de gestion_combustible",
    version="0.0.1"
)

#Routes para cada Entidad
app.include_router(rol_router)
app.include_router(tipo_combustible_router)
app.include_router(user)
app.include_router(user2)
app.include_router(vehiculos_router)
app.include_router(vehiculos_router2)
app.include_router(gasolineras_router)
app.include_router(proyecto_router)
app.include_router(bitacora_router)
app.include_router(bitacora_router2)
app.include_router(log_router)
