from enum import Enum


class ProductType(str, Enum):
    MANGA = "Manga"
    COMIC = "Cómic"
    FIGURA = "Figura"
    MERCHANDISING = "Merchandising"


class UserRole(str, Enum):
    ADMIN = "Admin"
    EMPLEADO = "Empleado"
    CLIENTE = "Cliente"


class StockMovementType(str, Enum):
    INGRESO = "Ingreso"
    VENTA = "Venta"
    AJUSTE = "Ajuste"
