# Sprint 2: Modelado de la Base de Datos (ERD) y Scripts SQL

**Proyecto:** Sistema Backend de Gestión de Inventarios y API REST  
**Destinatario:** Comercio / Distribuidora de Cómics, Manga, Figuras y Coleccionables.  
**Estado:** ✅ Completado  

---

## 1. Diccionario de Datos y Estructura Lógica

### 1.1. Tablas de Catálogo y Clasificación
* **`franquicias`**: `id` (PK, Integer, AI), `nombre` (VARCHAR(100), Unique, Not Null)
* **`editoriales`**: `id` (PK, Integer, AI), `nombre` (VARCHAR(100), Unique, Not Null)
* **`demografias`**: `id` (PK, Integer, AI), `nombre` (VARCHAR(100), Unique, Not Null)
* **`productos`**:
  * `id` (PK, Integer, AI)
  * `titulo_nombre` (VARCHAR(255), Not Null)
  * `descripcion` (TEXT, Nullable)
  * `precio_venta` (DECIMAL(10,2), Not Null)
  * `stock_actual` (INTEGER, Not Null, Default 0)
  * `tipo_producto` (VARCHAR(50), Not Null)
  * `id_franquicia` (INTEGER, FK -> franquicias.id, Not Null)
  * `numero_tomo` (VARCHAR(50), Nullable)
  * `id_editorial` (INTEGER, FK -> editoriales.id, Nullable)
  * `id_demografia` (INTEGER, FK -> demografias.id, Nullable)
  * `isbn` (VARCHAR(20), Unique, Nullable)
  * `marca_fabricante` (VARCHAR(100), Nullable)

### 1.2. Tablas de Usuarios y Seguridad
* **`usuarios`**:
  * `id` (PK, Integer, AI)
  * `email` (VARCHAR(255), Unique, Not Null)
  * `password_hash` (VARCHAR(255), Not Null)
  * `rol` (VARCHAR(50), Not Null)
  * `fecha_creacion` (TIMESTAMP, Default CURRENT_TIMESTAMP)
  * `activo` (BOOLEAN, Default TRUE)

### 1.3. Tablas de Operatividad y Auditoría
* **`movimientos_stock`**:
  * `id` (PK, Integer, AI)
  * `id_producto` (INTEGER, FK -> productos.id, Not Null)
  * `id_usuario` (INTEGER, FK -> usuarios.id, Not Null)
  * `tipo_movimiento` (VARCHAR(50), Not Null)
  * `cantidad` (INTEGER, Not Null, CHECK > 0)
  * `fecha_movimiento` (TIMESTAMP, Default CURRENT_TIMESTAMP)

---

## 2. Relaciones (Cardinalidad)

* **1 a N:** Una `franquicia` tiene muchos `productos`.
* **1 a N:** Una `editorial` tiene muchos `productos`.
* **1 a N:** Una `demografia` tiene muchos `productos`.
* **1 a N:** Un `usuario` registra muchos `movimientos_stock`.
* **1 a N:** Un `producto` tiene múltiples `movimientos_stock`.

---

## 3. Código DBML (dbdiagram.io)

```dbml
Table franquicias {
  id int [pk, increment]
  nombre varchar [unique, not null]
}

Table editoriales {
  id int [pk, increment]
  nombre varchar [unique, not null]
}

Table demografias {
  id int [pk, increment]
  nombre varchar [unique, not null]
}

Table productos {
  id int [pk, increment]
  titulo_nombre varchar [not null]
  descripcion text
  precio_venta decimal [not null]
  stock_actual int [not null, default: 0]
  tipo_producto varchar [not null]
  id_franquicia int [not null]
  numero_tomo varchar
  id_editorial int
  id_demografia int
  isbn varchar [unique]
  marca_fabricante varchar
}

Table usuarios {
  id int [pk, increment]
  email varchar [unique, not null]
  password_hash varchar [not null]
  rol varchar [not null]
  fecha_creacion timestamp
  activo boolean [default: true]
}

Table movimientos_stock {
  id int [pk, increment]
  id_producto int [not null]
  id_usuario int [not null]
  tipo_movimiento varchar [not null]
  cantidad int [not null]
  fecha_movimiento timestamp
}

Ref: productos.id_franquicia > franquicias.id
Ref: productos.id_editorial > editoriales.id
Ref: productos.id_demografia > demografias.id
Ref: movimientos_stock.id_producto > productos.id
Ref: movimientos_stock.id_usuario > usuarios.id
```

---

## 4. Script SQL DDL (PostgreSQL)

```sql
-- Tablas de Catálogo y Clasificación
CREATE TABLE IF NOT EXISTS franquicias (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS editoriales (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS demografias (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS productos (
    id SERIAL PRIMARY KEY,
    titulo_nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    precio_venta DECIMAL(10, 2) NOT NULL,
    stock_actual INTEGER NOT NULL DEFAULT 0,
    tipo_producto VARCHAR(50) NOT NULL,
    id_franquicia INTEGER NOT NULL,
    numero_tomo VARCHAR(50),
    id_editorial INTEGER,
    id_demografia INTEGER,
    isbn VARCHAR(20) UNIQUE,
    marca_fabricante VARCHAR(100),
    CONSTRAINT fk_franquicia FOREIGN KEY (id_franquicia) REFERENCES franquicias(id),
    CONSTRAINT fk_editorial FOREIGN KEY (id_editorial) REFERENCES editoriales(id),
    CONSTRAINT fk_demografia FOREIGN KEY (id_demografia) REFERENCES demografias(id)
);

-- Tablas de Usuarios y Seguridad
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    rol VARCHAR(50) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE
);

-- Tablas de Operatividad y Auditoría
CREATE TABLE IF NOT EXISTS movimientos_stock (
    id SERIAL PRIMARY KEY,
    id_producto INTEGER NOT NULL,
    id_usuario INTEGER NOT NULL,
    tipo_movimiento VARCHAR(50) NOT NULL,
    cantidad INTEGER NOT NULL CHECK (cantidad > 0),
    fecha_movimiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_producto FOREIGN KEY (id_producto) REFERENCES productos(id),
    CONSTRAINT fk_usuario FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
);
```
