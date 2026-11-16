# 📚 Sistema de Gestión de Inventarios y API REST (Cómics & Mangas)

Sistema backend profesional para la administración de inventario, catálogo, movimientos de stock y órdenes de un comercio especializado en cómics, mangas, figuras coleccionables y merchandising.

---

## 🛠️ Tecnologías Principales

* **Lenguaje:** Python 3.11+
* **Framework Web:** FastAPI (documentación automática Swagger/OpenAPI)
* **Servidor Web:** Uvicorn
* **Validación de Datos:** Pydantic v2
* **Base de Datos:** PostgreSQL
* **ORM:** SQLAlchemy 2.0 & Alembic (Migraciones)

---

## 🗓️ Plan de Trabajo y Estado de los Sprints (16 Semanas)

| Sprint | Semana | Módulo / Hito | Estado |
| :---: | :---: | :--- | :---: |
| **Sprint 1** | Semana 1 | Alcance y Definición de Historias de Usuario | ✅ Completado |
| **Sprint 2** | Semana 2 | Modelado de la Base de Datos (ERD, DBML, Scripts SQL DDL) | ✅ Completado |
| **Sprint 3** | Semana 3 | Setup del Proyecto, Repositorio Git y Arquitectura Base | ✅ Completado |
| **Sprint 4** | Semana 4 | Diseño del Contrato de la API (DTOs, Schemas y Swagger) | ✅ Completado |
| **Sprint 5** | Semana 5 | Conexión ORM (SQLAlchemy) y Migraciones (Alembic) | ✅ Completado |
| **Sprint 6** | Semana 6 | Módulo CRUD de Editoriales y Categorías | ⏳ Siguiente |
| **Sprint 7** | Semana 7 | Módulo CRUD de Catálogo de Productos (Manga / Cómics / Figuras) | ⏳ Pendiente |
| **Sprint 8** | Semana 8 | Buscador y Filtros Avanzados con Paginación | ⏳ Pendiente |
| **Sprint 9** | Semana 9 | Módulo de Usuarios, Roles y Cifrado de Contraseñas (Bcrypt) | ⏳ Pendiente |
| **Sprint 10** | Semana 10 | Autenticación JWT y Protección de Rutas | ⏳ Pendiente |
| **Sprint 11** | Semana 11 | Módulo de Movimientos de Inventario (Ingresos y Ventas) | ⏳ Pendiente |
| **Sprint 12** | Semana 12 | Alertas de Stock Mínimo | ⏳ Pendiente |
| **Sprint 13** | Semana 13 | Reportes y Métricas de Inventario | ⏳ Pendiente |
| **Sprint 14** | Semana 14 | Pruebas Unitarias e Integración con Pytest | ⏳ Pendiente |
| **Sprint 15** | Semana 15 | Despliegue en la Nube (Cloud Deployment) | ⏳ Pendiente |
| **Sprint 16** | Semana 16 | Cierre, Documentación Final y Presentación | ⏳ Pendiente |

---

## 📁 Estructura del Proyecto

```text
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   └── health.py       # Endpoint de verificación de salud
│   │       └── router.py           # Enrutador general v1
│   ├── core/
│   │   └── config.py               # Configuración y variables de entorno
│   ├── crud/                       # Operaciones a base de datos
│   ├── db/                         # Sesiones y configuración de BD
│   ├── models/                     # Modelos ORM SQLAlchemy
│   ├── schemas/                    # Esquemas y DTOs Pydantic
│   └── main.py                     # Punto de entrada de la aplicación FastAPI
├── docs/
│   └── sprints/                    # Documentación oficial de cada sprint
├── .env.example                    # Ejemplo de variables de entorno
├── .gitignore                      # Reglas de exclusión para Git
├── requirements.txt                # Dependencias del proyecto
└── README.md                       # Documentación general y seguimiento
```

---

## 🚀 Puesta en Marcha (Entorno Local)

### 1. Clonar el repositorio y acceder a la carpeta
```bash
git clone <URL_DEL_REPOSITORIO>
cd "PP Tp"
```

### 2. Crear y activar el entorno virtual
* **Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Instalar las dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Copiar `.env.example` a `.env`:
```bash
cp .env.example .env
```

### 5. Iniciar el servidor de desarrollo
```bash
uvicorn app.main:app --reload --port 8000
```

* **API Base:** [http://localhost:8000](http://localhost:8000)
* **Documentación Interactiva (Swagger UI):** [http://localhost:8000/api/v1/docs](http://localhost:8000/api/v1/docs)
* **Documentación Alternativa (ReDoc):** [http://localhost:8000/api/v1/redoc](http://localhost:8000/api/v1/redoc)
* **Health Check:** [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)
