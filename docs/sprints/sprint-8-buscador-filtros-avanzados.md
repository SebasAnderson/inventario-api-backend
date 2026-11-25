# Sprint 8: Buscador y Filtros Avanzados

**Proyecto:** Sistema Backend de Gestión de Inventarios y API REST  
**Destinatario:** Comercio / Distribuidora de Cómics, Manga, Figuras y Coleccionables.  
**Estado:** ✅ Completado  

---

## 1. Objetivos del Sprint

* [x] Implementar búsqueda combinada de productos (US-07) por `search` (título, descripción o ISBN), `titulo`, `numero_tomo` (coincidencia exacta insensible a mayúsculas), `isbn`, `tipo_producto`, `id_franquicia`, `id_editorial`, `id_demografia`, rango de precios (`precio_min`, `precio_max`) y disponibilidad (`en_stock`).
* [x] Agregar ordenamiento determinista (`sort_by`: `id`, `titulo_nombre`, `precio_venta`, `stock_actual`; `sort_order`: `asc`, `desc`).
* [x] Implementar el endpoint dedicado `GET /api/v1/products/search` con paginación por páginas (`page`, `limit`) y metadatos (`total`, `page`, `limit`, `total_pages`, `has_next`, `has_prev`, `items`).
* [x] Integrar los mismos filtros combinados en `GET /api/v1/products/` manteniendo la compatibilidad del contrato (`List[ProductResponse]`) y escapando caracteres especiales (`%`, `_`, `\`) en consultas `ILIKE`.
* [x] Escribir suite de pruebas automatizadas (`tests/test_product_search.py`) y verificar funcionamiento real contra PostgreSQL.

---

## 2. Archivos Creados / Modificados

* `app/schemas/common.py`, `app/schemas/product.py`, `app/schemas/__init__.py`: Enums `ProductSortBy` y `SortOrder`, esquema `ProductFilters` y respuesta paginada `ProductSearchResponse`.
* `app/crud/product.py`: Motor de filtros `_apply_filters`, escape de comodines `_escape_like` y método `search` con conteo total y ordenamiento determinista.
* `app/api/v1/endpoints/products.py`: Dependencia compartida `get_product_filters`, endpoint `GET /api/v1/products/search` y soporte completo de filtros en `GET /api/v1/products/`.
* `tests/test_product_search.py`, `tests/test_api_contract.py`: Pruebas de búsqueda, filtros combinados, ordenamiento, paginación y validación de rango de precios.

---

## 3. Verificación y Testing

```text
tests/test_api_contract.py .... [ 23%]
tests/test_catalog_crud.py ....... [ 64%]
tests/test_product_crud.py ... [ 82%]
tests/test_product_search.py ... [100%]
17 passed in 1.05s
```
* Smoke test end-to-end ejecutado contra PostgreSQL (`comic_store_db`, puerto `5229`): búsqueda combinada, coincidencia de `"Tomo Único"` y escape de `"%"` verificados correctamente.
