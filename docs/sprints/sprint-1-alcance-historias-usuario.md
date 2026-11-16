# Sprint 1: Alcance e Historias de Usuario

**Proyecto:** Sistema Backend de Gestión de Inventarios y API REST  
**Destinatario:** Comercio / Distribuidora de Cómics, Manga, Figuras y Coleccionables.  
**Estado:** ✅ Completado  

---

## 1. Roles del Sistema y Permisos Generales

El sistema operará con tres (3) niveles de acceso o roles, con permisos claramente diferenciados:

* **Administrador (Owner/Dueño):**
  * Control absoluto sobre la plataforma (Superusuario).
  * Permiso exclusivo para gestionar cuentas de usuarios del sistema (Alta, suspensión, modificación de permisos o baja lógica de Empleados y Clientes).
  * Gestión completa de inventario y configuración de la tienda.
* **Empleado:**
  * Control total sobre la operativa diaria del negocio a través de la API.
  * Operaciones CRUD sobre productos del catálogo, clasificaciones y actualización de stock.
  * Sin acceso al módulo de gestión de usuarios ni alteración de permisos.
* **Cliente:**
  * Rol de usuario final.
  * Registro de cuenta, inicio de sesión y modificación de perfil básico.
  * Permisos limitados a lectura (navegar por el catálogo, utilizar filtros de búsqueda) y creación de órdenes/compras.

---

## 2. Historias de Usuario (User Stories)

### Módulo de Gestión de Usuarios y Accesos
* **US-01: Gestión de cuentas (Admin)**
  * *Historia:* Como Administrador, quiero dar de alta, suspender o eliminar cuentas de empleados y clientes para controlar quién tiene acceso al sistema y con qué permisos.
  * *Criterios de aceptación:* La API debe exponer endpoints protegidos solo accesibles para el rol Admin. No se eliminarán registros físicos de clientes con historial de compras (Soft Delete/Baja lógica).
* **US-02: Registro de clientes**
  * *Historia:* Como Cliente, quiero registrarme en la plataforma mediante un correo electrónico y contraseña para poder acceder al catálogo y realizar compras.

### Módulo de Gestión de Catálogo
* **US-03: Mantenimiento del catálogo (Empleado/Admin)**
  * *Historia:* Como Empleado, quiero crear, editar o eliminar productos del inventario para mantener la oferta de la tienda actualizada.
  * *Criterios de aceptación:* El sistema debe admitir tanto artículos de lectura (cómics/mangas) como artículos de colección (figuras/merchandising). Los campos obligatorios de ingreso variarán según el tipo de producto.
* **US-04: Clasificación avanzada (Empleado/Admin)**
  * *Historia:* Como Empleado, quiero clasificar los productos por Editorial, Franquicia y Demografía para facilitar la búsqueda y organización.
  * *Criterios de aceptación:* Se deben poder gestionar (CRUD) las listas de Editoriales, Franquicias y Demografías de manera independiente.

### Módulo de Operaciones de Stock y Compras
* **US-05: Ingreso de mercadería (Empleado/Admin)**
  * *Historia:* Como Empleado, quiero registrar el ingreso de nueva mercadería al inventario general para que las cantidades disponibles aumenten de forma inmediata.
  * *Criterios de aceptación:* La operación sumará el valor ingresado al stock actual del producto.
* **US-06: Compra de productos (Cliente)**
  * *Historia:* Como Cliente, quiero realizar una compra para adquirir los productos deseados, de modo que el sistema procese la orden y actualice el inventario.
  * *Criterios de aceptación:* El sistema debe validar que exista stock suficiente antes de confirmar la compra. El stock se descontará automáticamente al concretarse la orden.
* **US-07: Navegación y búsqueda (Cliente)**
  * *Historia:* Como Cliente, quiero navegar por el catálogo utilizando filtros combinados (Franquicia, Editorial, Demografía) para encontrar productos específicos rápidamente.

### Módulo de Alertas
* **US-08: Alertas de stock (Empleado/Admin)**
  * *Historia:* Como Empleado, quiero visualizar una lista automática de todos los productos cuyo stock sea igual o inferior a un umbral predefinido para saber qué artículos debo reponer.
  * *Criterios de aceptación:* Se utilizará una regla global en el sistema (ej. alertar si Stock <= 3) calculada al momento de la consulta.

---

## 3. Estructura de Datos (Diccionario de Entidades)

### Entidad Principal: `PRODUCTO`
* `id_producto` (Integer / PK): Identificador único autoincremental.
* `titulo_nombre` (String, Not Null): Nombre descriptivo del artículo.
* `descripcion` (Text, Nullable): Detalles adicionales y sinopsis.
* `precio_venta` (Decimal, Not Null): Precio unitario de venta al público.
* `stock_actual` (Integer, Not Null, Default 0): Cantidad de unidades físicas disponibles.
* `tipo_producto` (Enum, Not Null): `['Manga', 'Cómic', 'Figura', 'Merchandising']`.
* `id_franquicia` (Integer, Not Null, FK): Referencia a la tabla de franquicias.

#### Atributos Específicos:
* **Lectura (Manga/Cómic):**
  * `numero_tomo` (Integer/String, Nullable): Número del volumen.
  * `id_editorial` (Integer, Nullable, FK): Referencia a editoriales.
  * `id_demografia` (Integer, Nullable, FK): Referencia a demografías.
  * `isbn` (String, Unique, Nullable): Código normalizado internacional.
* **Coleccionables (Figuras/Merchandising):**
  * `marca_fabricante` (String, Nullable): Empresa fabricante.
