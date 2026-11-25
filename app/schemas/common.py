from enum import Enum


class ProductType(str, Enum):
    MANGA = "Manga"
    COMIC = "Cómic"
    FIGURA = "Figura"
    MERCHANDISING = "Merchandising"


class ProductSortBy(str, Enum):
    ID = "id"
    TITULO = "titulo_nombre"
    PRECIO = "precio_venta"
    STOCK = "stock_actual"


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


class UserRole(str, Enum):
    ADMIN = "Admin"
    EMPLEADO = "Empleado"
    CLIENTE = "Cliente"


class StockMovementType(str, Enum):
    INGRESO = "Ingreso"
    VENTA = "Venta"
    AJUSTE = "Ajuste"
