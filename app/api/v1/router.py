from fastapi import APIRouter
from app.api.v1.endpoints import (
    health,
    auth,
    users,
    publishers,
    franchises,
    demographics,
    products,
    stock
)

api_router = APIRouter()

# Registro ordenado de módulos para el contrato de la API (OpenAPI / Swagger)
api_router.include_router(health.router, prefix="", tags=["Health"])
api_router.include_router(auth.router, prefix="/auth", tags=["Autenticación"])
api_router.include_router(users.router, prefix="/users", tags=["Usuarios"])
api_router.include_router(publishers.router, prefix="/publishers", tags=["Editoriales"])
api_router.include_router(franchises.router, prefix="/franchises", tags=["Franquicias"])
api_router.include_router(demographics.router, prefix="/demographics", tags=["Demografías"])
api_router.include_router(products.router, prefix="/products", tags=["Productos & Catálogo"])
api_router.include_router(stock.router, prefix="/stock", tags=["Movimientos de Inventario"])
