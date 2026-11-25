# Sprint 6: Módulo CRUD de Editoriales y Categorías

**Proyecto:** Sistema Backend de Gestión de Inventarios y API REST  
**Destinatario:** Comercio / Distribuidora de Cómics, Manga, Figuras y Coleccionables.  
**Estado:** ✅ Completado  

---

## 1. Objetivos del Sprint

* [x] Implementar la capa CRUD genérica reutilizable (`app/crud/base.py`) para operaciones en PostgreSQL mediante SQLAlchemy.
* [x] Implementar los repositorios CRUD específicos para **Editoriales** (`Publisher`), **Franquicias** (`Franchise`) y **Demografías** (`Demographic`).
* [x] Reemplazar los datos mock del Sprint 4 en `/api/v1/publishers`, `/api/v1/franchises` y `/api/v1/demographics` por persistencia real en PostgreSQL usando inyección de sesión (`get_db`).
* [x] Añadir validaciones de negocio e integridad:
  * Limpieza de espacios en blanco y rechazo de nombres vacíos (`422 Unprocessable Entity`).
  * Prevención de duplicados insensible a mayúsculas/minúsculas (`400 Bad Request`).
  * Manejo de recursos inexistentes (`404 Not Found`).
  * Paginación controlada (`skip >= 0`, `1 <= limit <= 100`).
  * Bloqueo de eliminación cuando existen productos asociados (`400 Bad Request`).
* [x] Crear suite de pruebas automatizadas (`tests/test_catalog_crud.py`) y verificar flujo real contra PostgreSQL.

---

## 2. Archivos Creados / Modificados

* `app/crud/base.py`: Clases genéricas `CRUDBase` y `CatalogCRUD` con ordenamiento determinista por `id` y búsqueda case-insensitive por `nombre`.
* `app/crud/publisher.py`, `app/crud/franchise.py`, `app/crud/demographic.py`, `app/crud/__init__.py`: Instancias CRUD de las tablas de clasificación.
* `app/api/v1/catalog_helpers.py`: Helpers compartidos para validación de unicidad, 404, manejo de `IntegrityError` y protección de borrado con productos vinculados.
* `app/api/v1/endpoints/publishers.py`, `franchises.py`, `demographics.py`: Endpoints conectados a PostgreSQL.
* `app/schemas/publisher.py`, `franchise.py`, `demographic.py`: Validación `min_length=1` y `str_strip_whitespace=True`.
* `tests/test_catalog_crud.py`: 7 casos de prueba parametrizados cubriendo ciclo completo CRUD, validaciones y restricciones de integridad.

---

## 3. Verificación y Testing

```text
tests/test_api_contract.py .... [ 36%]
tests/test_catalog_crud.py ....... [100%]
11 passed in 1.15s
```
* Smoke test end-to-end ejecutado contra PostgreSQL (`comic_store_db`, puerto `5229`): creación, lectura y eliminación verificadas exitosamente.
