# Sprint 4: Diseño del Contrato de la API (OpenAPI / Swagger y Schemas DTO)

**Proyecto:** Sistema Backend de Gestión de Inventarios y API REST  
**Destinatario:** Comercio / Distribuidora de Cómics, Manga, Figuras y Coleccionables.  
**Estado:** ✅ Completado  

---

## 1. Objetivos del Sprint

* [x] Diseñar la estructura general de rutas de la API bajo el prefijo unificado `/api/v1`.
* [x] Documentar e implementar los esquemas de entrada y salida de datos (DTOs) con **Pydantic v2**.
* [x] Establecer validaciones de tipo, restricciones de longitud, tipos de productos (Enum) y reglas de negocio preliminares (precios > 0, stock >= 0).
* [x] Exponer la especificación interactiva completa de **OpenAPI / Swagger UI** (`/api/v1/docs`) y **ReDoc** (`/api/v1/redoc`).
* [x] Implementar respuestas mock tipadas para permitir la inspección interactiva del contrato sin depender aún de la base de datos física.
* [x] Escribir suite de pruebas unitarias (`tests/test_api_contract.py`) para validar la generación correcta de OpenAPI y contratos clave.

---

## 2. Mapa de Endpoints del Contrato de la API (`/api/v1`)

### 2.1. Módulo de Autenticación (`/auth`)
| Método | Endpoint | Descripción | Entrada (DTO) | Salida (DTO) | Códigos HTTP |
| :---: | :--- | :--- | :--- | :--- | :---: |
| `POST` | `/api/v1/auth/login` | Iniciar sesión y obtener token JWT | `LoginRequest` | `TokenResponse` | 200, 401 |

### 2.2. Módulo de Usuarios (`/users`)
| Método | Endpoint | Descripción | Entrada (DTO) | Salida (DTO) | Códigos HTTP |
| :---: | :--- | :--- | :--- | :--- | :---: |
| `GET` | `/api/v1/users/` | Listar usuarios (Admin) | - | `List[UserResponse]` | 200, 401, 403 |
| `POST` | `/api/v1/users/` | Crear nuevo usuario | `UserCreate` | `UserResponse` | 201, 400 |
| `GET` | `/api/v1/users/{user_id}` | Obtener detalle de usuario | - | `UserResponse` | 200, 404 |
| `PUT` | `/api/v1/users/{user_id}` | Modificar datos de usuario | `UserUpdate` | `UserResponse` | 200, 400, 404 |
| `DELETE` | `/api/v1/users/{user_id}` | Baja lógica (Soft Delete) | - | `UserResponse` | 200, 404 |

### 2.3. Módulo de Catálogo y Clasificación (`/publishers`, `/franchises`, `/demographics`)
| Módulo | Métodos Soportados | Esquema Entrada | Esquema Salida |
| :--- | :--- | :--- | :--- |
| **Editoriales** | `GET /`, `POST /`, `GET /{id}`, `PUT /{id}`, `DELETE /{id}` | `PublisherCreate`, `PublisherUpdate` | `PublisherResponse` |
| **Franquicias** | `GET /`, `POST /`, `GET /{id}`, `PUT /{id}`, `DELETE /{id}` | `FranchiseCreate`, `FranchiseUpdate` | `FranchiseResponse` |
| **Demografías** | `GET /`, `POST /`, `GET /{id}`, `PUT /{id}`, `DELETE /{id}` | `DemographicCreate`, `DemographicUpdate` | `DemographicResponse` |

### 2.4. Módulo de Productos (`/products`)
| Método | Endpoint | Descripción | Entrada (DTO) | Salida (DTO) | Códigos HTTP |
| :---: | :--- | :--- | :--- | :--- | :---: |
| `GET` | `/api/v1/products/` | Listar productos con filtros y paginación | Query params (`skip`, `limit`, `tipo`, etc.) | `List[ProductResponse]` | 200 |
| `POST` | `/api/v1/products/` | Crear un nuevo producto | `ProductCreate` | `ProductResponse` | 201, 400 |
| `GET` | `/api/v1/products/low-stock` | Alertas de productos bajo stock mínimo | Query param `threshold` | `List[LowStockAlert]` | 200 |
| `GET` | `/api/v1/products/{product_id}` | Obtener producto por ID | - | `ProductResponse` | 200, 404 |
| `PUT` | `/api/v1/products/{product_id}` | Modificar producto existente | `ProductUpdate` | `ProductResponse` | 200, 400, 404 |
| `DELETE` | `/api/v1/products/{product_id}` | Eliminar producto del catálogo | - | - | 204, 404 |

### 2.5. Módulo de Movimientos de Inventario (`/stock`)
| Método | Endpoint | Descripción | Entrada (DTO) | Salida (DTO) | Códigos HTTP |
| :---: | :--- | :--- | :--- | :--- | :---: |
| `GET` | `/api/v1/stock/movements` | Historial de movimientos | Query params (`id_producto`, `tipo_movimiento`) | `List[StockMovementResponse]` | 200 |
| `POST` | `/api/v1/stock/movements` | Registrar ingreso, venta o ajuste | `StockMovementCreate` | `StockMovementResponse` | 201, 400 |

---

## 3. Verificación y Resultados de Testing

Se ejecutó la suite de pruebas unitarias validando la consistencia del contrato OpenAPI:
```text
tests/test_api_contract.py .... [100%]
4 passed in 0.27s
```
* La documentación interactiva Swagger UI está disponible en: `http://localhost:8000/api/v1/docs`
