# Sprint 3: Setup del Proyecto y Repositorio

**Proyecto:** Sistema Backend de Gestión de Inventarios y API REST  
**Destinatario:** Comercio / Distribuidora de Cómics, Manga, Figuras y Coleccionables.  
**Estado:** ✅ Completado  

---

## 1. Objetivos del Sprint

* [x] Inicializar repositorio local de Git con `.gitignore` adecuado.
* [x] Versionar la documentación de Sprint 1, Sprint 2 y Sprint 3.
* [x] Definir la arquitectura limpia de directorios para FastAPI.
* [x] Crear y activar el entorno virtual de Python (`venv`).
* [x] Especificar e instalar las dependencias requeridas en `requirements.txt`.
* [x] Configurar variables de entorno (`.env.example` y `.env`).
* [x] Crear una aplicación base FastAPI con endpoint de verificación (`GET /api/v1/health`).
* [x] Configurar el archivo `README.md` con la tabla de seguimiento de los 16 Sprints.


---

## 2. Decisiones Técnicas

* **Framework Web:** FastAPI (documentación Swagger/OpenAPI automática, validación mediante Pydantic, alto rendimiento asíncrono).
* **Servidor ASGI:** Uvicorn.
* **ORM:** SQLAlchemy (preparado para Sprint 5).
* **Migraciones:** Alembic (preparado para Sprint 5).
* **Driver PostgreSQL:** `psycopg2-binary`.
* **Configuración:** `pydantic-settings` y `python-dotenv`.
