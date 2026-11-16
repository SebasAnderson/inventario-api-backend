# Sprint 5: Conexión ORM y Migraciones

**Proyecto:** Sistema Backend de Gestión de Inventarios y API REST  
**Destinatario:** Comercio / Distribuidora de Cómics, Manga, Figuras y Coleccionables.  
**Estado:** ✅ Completado  

---

## 1. Objetivos del Sprint

* [x] Configurar la conexión a PostgreSQL mediante SQLAlchemy 2.0 con el driver `psycopg2-binary`.
* [x] Crear los 6 modelos ORM correspondientes al ERD del Sprint 2.
* [x] Inicializar y configurar Alembic para versionado de migraciones de base de datos.
* [x] Escribir y ejecutar la migración inicial (`0001_initial_schema`) que crea las 6 tablas físicas.
* [x] Verificar la creación correcta de tablas, columnas, relaciones y constraints en PostgreSQL.

---

## 2. Modelos ORM Implementados (SQLAlchemy 2.0)

| Modelo | Tabla | Archivo | Relaciones |
| :--- | :--- | :--- | :--- |
| `Publisher` | `editoriales` | `app/models/publisher.py` | 1:N → `productos` |
| `Franchise` | `franquicias` | `app/models/franchise.py` | 1:N → `productos` |
| `Demographic` | `demografias` | `app/models/demographic.py` | 1:N → `productos` |
| `Product` | `productos` | `app/models/product.py` | N:1 → franquicia, editorial, demografía; 1:N → movimientos |
| `User` | `usuarios` | `app/models/user.py` | 1:N → `movimientos_stock` |
| `StockMovement` | `movimientos_stock` | `app/models/stock_movement.py` | N:1 → producto, usuario |

---

## 3. Configuración de Base de Datos

* **Motor:** PostgreSQL 18 (puerto 5229)
* **Base de datos:** `comic_store_db`
* **ORM:** SQLAlchemy 2.0 con estilo declarativo (`Mapped`, `mapped_column`)
* **Sesión:** `app/db/session.py` con inyección de dependencias (`get_db`) para FastAPI
* **Driver:** `psycopg2-binary` (especificado como `postgresql+psycopg2://` en la URL)

---

## 4. Alembic y Migración Inicial

* Configuración en `alembic/env.py` con carga dinámica de la URL desde `app.core.config.settings`.
* Migración `0001_initial_schema.py` ejecutada exitosamente:
  * 6 tablas creadas: `franquicias`, `editoriales`, `demografias`, `usuarios`, `productos`, `movimientos_stock`
  * Índices, Foreign Keys y CHECK constraints aplicados correctamente.

---

## 5. Verificación

```text
=== TABLES IN comic_store_db ===
  - alembic_version
  - demografias
  - editoriales
  - franquicias
  - movimientos_stock
  - productos
  - usuarios
```
Todas las tablas visibles desde pgAdmin y verificadas mediante consulta a `information_schema.tables`.
