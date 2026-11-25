# Sprint 7: Módulo CRUD de Catálogo de Productos

**Proyecto:** Sistema Backend de Gestión de Inventarios y API REST  
**Destinatario:** Comercio / Distribuidora de Cómics, Manga, Figuras y Coleccionables.  
**Estado:** ✅ Completado  

---

## 1. Objetivos del Sprint

* [x] Implementar el repositorio CRUD de productos (`app/crud/product.py`) heredando de `CRUDBase` con soporte para búsqueda por ISBN.
* [x] Conectar los endpoints CRUD de `/api/v1/products/` (`GET`, `POST`, `GET /{product_id}`, `PUT /{product_id}`, `DELETE /{product_id}`) a PostgreSQL mediante SQLAlchemy.
* [x] Aplicar validaciones de datos de entrada y reglas de negocio (US-03):
  * Precio de venta estrictamente positivo (`precio_venta > 0`, `max_digits=10`, `decimal_places=2`) y stock inicial no negativo (`stock_actual >= 0`).
  * Validación dinámica de campos obligatorios por `tipo_producto` tanto en alta (`POST`) como en actualización parcial (`PUT`):
    * `Manga` y `Cómic`: requieren `id_editorial` y `numero_tomo`.
    * `Figura` y `Merchandising`: requieren `marca_fabricante`.
  * Normalización de cadenas vacías en campos opcionales (`isbn`, `numero_tomo`, `marca_fabricante`, `descripcion`) a `None` y rechazo de valores `null` en campos obligatorios al actualizar.
  * Unicidad de `isbn` (`400 Bad Request`) y verificación de existencia de claves foráneas (`id_franquicia`, `id_editorial`, `id_demografia`).
  * Protección contra borrado físico cuando existen movimientos de stock asociados (`400 Bad Request`).
* [x] Escribir suite de pruebas automatizadas (`tests/test_product_crud.py`) y validar flujo real contra PostgreSQL.

---

## 2. Archivos Creados / Modificados

* `app/crud/product.py`, `app/crud/__init__.py`: Clase `ProductCRUD` (`get_by_isbn`, `create`, `update`) e instancia exportada `product`.
* `app/schemas/product.py`: Validaciones de entrada/salida, `validate_product_type_requirements`, normalización de strings vacíos y protección contra nulos en `ProductUpdate`.
* `app/api/v1/endpoints/products.py`: Endpoints CRUD reales sobre PostgreSQL (manteniendo el contrato mock de `/low-stock` para el Sprint 12).
* `tests/test_product_crud.py`, `tests/test_api_contract.py`: Pruebas unitarias de ciclo completo CRUD, validaciones y restricciones de integridad.

---

## 3. Verificación y Testing

```text
tests/test_api_contract.py .... [ 28%]
tests/test_catalog_crud.py ....... [ 78%]
tests/test_product_crud.py ... [100%]
14 passed in 0.98s
```
* Smoke test end-to-end ejecutado contra PostgreSQL (`comic_store_db`, puerto `5229`): alta de producto editorial, modificación de precio y limpieza verificadas correctamente.
