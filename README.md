# Punto de venta

Proyecto web para administrar un punto de venta con inventario, catalogos, usuarios y registro de ventas.

## Stack

- Backend: Django, Django REST Framework, Simple JWT
- Base de datos: MySQL
- Frontend: Vue 3, Vite, Bootstrap, Axios

## Modelo de datos

El backend sigue el modelo de `BD_PUNTOVENTA.pdf`:

- `roles`
- `usuarios`
- `categorias`
- `marcas`
- `tallas`
- `colores`
- `productos`
- `variantes_producto`
- `ventas`
- `detalle_ventas`

Relaciones principales:

- Un usuario pertenece a un rol.
- Un producto pertenece a una categoria y a una marca.
- Una variante pertenece a un producto, una talla y un color.
- Una venta pertenece a un usuario.
- Un detalle de venta pertenece a una venta y a una variante.

## Estructura

```text
backend/
  core/        Configuracion principal de Django
  productos/  Catalogos, productos y variantes
  usuarios/   Roles, usuarios del modelo y autenticacion JWT
  ventas/     Registro de ventas y detalles
frontend/
  src/         Aplicacion Vue
```

## Configuracion del backend

Crear un archivo `backend/.env` tomando como base `backend/.env.example`.

Ejemplo:

```text
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DB_ENGINE=django.db.backends.mysql
DB_NAME=db_punto_venta
DB_USER=root
DB_PASSWORD=12345
DB_HOST=127.0.0.1
DB_PORT=3306
```

Instalar dependencias:

```bash
cd backend
python -m pip install -r requirements.txt
```

Aplicar migraciones:

```bash
python manage.py migrate
```

Crear administrador:

```bash
python manage.py createsuperuser
```

Ejecutar backend:

```bash
python manage.py runserver 127.0.0.1:8000
```

## Configuracion del frontend

Instalar dependencias:

```bash
cd frontend
npm install
```

Ejecutar frontend:

```bash
npm run dev -- --host 127.0.0.1
```

La aplicacion consume la API en:

```text
http://127.0.0.1:8000/api/
```

## Endpoints principales

```text
POST /api/auth/login/
POST /api/auth/refresh/
GET  /api/auth/me/

GET/POST /api/roles/
GET/POST /api/usuarios/
GET/POST /api/categorias/
GET/POST /api/marcas/
GET/POST /api/tallas/
GET/POST /api/colores/
GET/POST /api/productos/
GET/POST /api/variantes/
GET/POST /api/ventas/
```

## Pruebas

Backend:

```bash
cd backend
python manage.py check
python manage.py test
```

Frontend:

```bash
cd frontend
npm run build
```

## Flujo de uso

1. Crear roles.
2. Crear usuarios del punto de venta.
3. Crear catalogos: categorias, marcas, tallas y colores.
4. Crear productos.
5. Crear variantes con SKU, codigo de barras, precio y stock.
6. Registrar ventas seleccionando usuario, variante, cantidad y metodo de pago.
