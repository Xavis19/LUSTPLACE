# 🚀 COMANDOS ÚTILES - LUSTPLACE

## 📋 Índice Rápido
- [Configuración Inicial](#configuración-inicial)
- [Gestión de Base de Datos](#gestión-de-base-de-datos)
- [Servidor de Desarrollo](#servidor-de-desarrollo)
- [Testing](#testing)
- [Admin](#admin)
- [Troubleshooting](#troubleshooting)

---

## 🔧 Configuración Inicial

### 1. Clonar y Configurar Entorno

```bash
# Navegar al proyecto
cd /Users/editsongutierreza/Downloads/LUSTPLACE/LUSTPLACE

# Activar entorno virtual
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar Variables de Entorno

```bash
# Copiar ejemplo de variables
cp .env.example .env

# Editar variables (usar nano, vim o VSCode)
nano .env
```

---

## 💾 Gestión de Base de Datos

### Migraciones

```bash
# Ver estado de migraciones
python manage.py showmigrations

# Ver migraciones de productos específicamente
python manage.py showmigrations productos

# Crear nuevas migraciones
python manage.py makemigrations

# Crear migración para app específica
python manage.py makemigrations productos

# Aplicar migraciones
python manage.py migrate

# Aplicar migración específica
python manage.py migrate productos

# Ver SQL de migración
python manage.py sqlmigrate productos 0005
```

### Resetear Base de Datos

```bash
# ⚠️ CUIDADO: Esto borra TODOS los datos

# Opción 1: Borrar archivo de BD
rm db.sqlite3
python manage.py migrate

# Opción 2: Flush (vaciar pero mantener estructura)
python manage.py flush

# Recrear migraciones desde cero
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
python manage.py makemigrations
python manage.py migrate
```

### Datos de Prueba

```bash
# Crear superusuario
python manage.py createsuperuser

# Cargar datos de prueba (si existe fixture)
python manage.py loaddata productos_fixture.json

# Crear fixture desde datos actuales
python manage.py dumpdata productos.Producto --indent 2 > productos_fixture.json
```

---

## 🌐 Servidor de Desarrollo

### Iniciar Servidor

```bash
# Servidor normal (puerto 8000)
python manage.py runserver

# Servidor en puerto específico
python manage.py runserver 8080

# Servidor accesible desde red local
python manage.py runserver 0.0.0.0:8000
```

### Collectstatic

```bash
# Recolectar archivos estáticos
python manage.py collectstatic

# Forzar recolección (sobrescribir)
python manage.py collectstatic --clear --noinput
```

---

## 🧪 Testing

### Ejecutar Tests

```bash
# Todos los tests
python manage.py test

# Tests de app específica
python manage.py test productos

# Test específico
python manage.py test productos.tests.TestProductoModel

# Con verbosidad
python manage.py test --verbosity=2

# Con coverage (instalar: pip install coverage)
coverage run --source='.' manage.py test
coverage report
coverage html  # Genera reporte HTML
```

---

## 👤 Admin

### Gestión de Usuarios

```bash
# Crear superusuario
python manage.py createsuperuser
# Usuario: admin
# Email: admin@lustplace.com
# Password: (ingresar)

# Cambiar contraseña de usuario
python manage.py changepassword admin

# Crear usuario normal por shell
python manage.py shell
>>> from django.contrib.auth.models import User
>>> user = User.objects.create_user('usuario', 'email@example.com', 'password')
>>> user.save()
>>> exit()
```

### Acceder al Admin

```bash
# Iniciar servidor
python manage.py runserver

# Abrir en navegador:
# http://127.0.0.1:8000/admin/

# Credenciales:
# Usuario: admin
# Password: (tu contraseña)
```

---

## 🔍 Inspección y Debug

### Django Shell

```bash
# Abrir shell interactivo
python manage.py shell

# Ejemplos de uso:
>>> from productos.models import Producto, Resena
>>> Producto.objects.all()
>>> Producto.objects.filter(mas_vendido=True)
>>> p = Producto.objects.first()
>>> p.porcentaje_stock_vendido
>>> p.imagenes_galeria
>>> p.get_colores_lista()
```

### DBShell

```bash
# Abrir shell de base de datos
python manage.py dbshell

# Comandos SQLite útiles:
.tables                    # Ver todas las tablas
.schema productos_producto # Ver estructura de tabla
SELECT * FROM productos_producto LIMIT 5;
.exit
```

### Check del Proyecto

```bash
# Verificar problemas del proyecto
python manage.py check

# Check completo (incluye deployment)
python manage.py check --deploy

# Check de app específica
python manage.py check productos
```

---

## 📊 Datos y Queries

### Crear Productos de Prueba

```python
# python manage.py shell

from productos.models import Producto, Categoria

# Crear categoría
cat = Categoria.objects.create(nombre="Juguetes", descripcion="Juguetes para adultos")

# Crear producto con todas las mejoras
p = Producto.objects.create(
    nombre="Producto de Prueba",
    descripcion="Descripción del producto",
    categoria=cat,
    precio=99.99,
    precio_oferta=79.99,
    stock=50,
    vendidos=150,
    nuevo=True,
    mas_vendido=True,
    colores_disponibles="Rojo#FF0000,Negro#000000,Rosa#FF69B4"
)

print(f"Producto creado: {p.nombre}")
print(f"% vendido: {p.porcentaje_stock_vendido}%")
print(f"Colores: {p.get_colores_lista()}")
```

### Actualizar Productos Masivamente

```python
# python manage.py shell

from productos.models import Producto

# Marcar todos como activos
Producto.objects.all().update(activo=True)

# Agregar 50 vendidos a productos destacados
Producto.objects.filter(destacado=True).update(vendidos=50)

# Marcar top 5 como más vendidos
top_productos = Producto.objects.order_by('-vendidos')[:5]
for p in top_productos:
    p.mas_vendido = True
    p.save()
```

---

## 🛠️ Troubleshooting

### Error: "No module named 'django'"

```bash
# Asegurarse de que el entorno virtual está activado
source .venv/bin/activate

# Reinstalar Django
pip install django
```

### Error: "Migrations not applied"

```bash
# Aplicar todas las migraciones pendientes
python manage.py migrate

# Si hay conflictos, verificar:
python manage.py showmigrations
```

### Error: "Static files not found"

```bash
# Recolectar archivos estáticos
python manage.py collectstatic --noinput

# Verificar configuración en settings.py:
# STATIC_URL = '/static/'
# STATIC_ROOT = BASE_DIR / 'staticfiles'
```

### Error: "Port already in use"

```bash
# Encontrar proceso en puerto 8000
lsof -i :8000

# Matar proceso
kill -9 <PID>

# O usar otro puerto
python manage.py runserver 8080
```

### Limpiar __pycache__

```bash
# Eliminar todos los archivos de cache
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete
```

### Reset de Migraciones de una App

```bash
# ⚠️ CUIDADO: Esto puede causar pérdida de datos

# 1. Borrar migraciones de la app
rm productos/migrations/0*.py

# 2. Borrar tablas de la base de datos
python manage.py dbshell
# En SQLite:
DROP TABLE productos_producto;
DROP TABLE productos_categoria;
DROP TABLE productos_resena;
# ... etc
.exit

# 3. Recrear migraciones
python manage.py makemigrations productos
python manage.py migrate productos
```

---

## 📦 Gestión de Dependencias

### Actualizar Requirements

```bash
# Congelar dependencias actuales
pip freeze > requirements.txt

# Instalar desde requirements
pip install -r requirements.txt

# Actualizar paquete específico
pip install --upgrade django

# Ver paquetes instalados
pip list

# Ver paquetes desactualizados
pip list --outdated
```

---

## 🔐 Seguridad

### Generar SECRET_KEY Nueva

```python
# python manage.py shell

from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### Cambiar Contraseñas

```bash
# Cambiar contraseña de superusuario
python manage.py changepassword admin

# Desde shell
python manage.py shell
>>> from django.contrib.auth.models import User
>>> u = User.objects.get(username='admin')
>>> u.set_password('nueva_password')
>>> u.save()
```

---

## 📊 Performance

### Ver Queries SQL

```python
# En shell o views.py (solo DEBUG=True)

from django.db import connection
from productos.models import Producto

# Hacer query
productos = list(Producto.objects.all())

# Ver queries ejecutadas
print(connection.queries)
print(f"Total queries: {len(connection.queries)}")
```

### Optimizar Queries

```python
# Mal (N+1 queries)
productos = Producto.objects.all()
for p in productos:
    print(p.categoria.nombre)  # Query por cada producto

# Bien (1 query)
productos = Producto.objects.select_related('categoria')
for p in productos:
    print(p.categoria.nombre)  # Sin queries adicionales
```

---

## 🚀 Deployment

### Preparar para Producción

```bash
# 1. Actualizar requirements
pip freeze > requirements.txt

# 2. Collectstatic
python manage.py collectstatic --noinput

# 3. Verificar deployment checklist
python manage.py check --deploy

# 4. Crear backup de BD
cp db.sqlite3 db.sqlite3.backup

# 5. Desactivar DEBUG en settings.py
# DEBUG = False
# ALLOWED_HOSTS = ['tudominio.com']
```

---

## 📝 Logs

### Ver Logs en Desarrollo

```bash
# Logs en consola del servidor
python manage.py runserver
# Los logs aparecerán aquí

# Habilitar logs de SQL en settings.py:
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

---

## 🎯 Comandos Personalizados (Útiles)

### Poblar BD con Datos de Prueba

```bash
# Crear archivo: productos/management/commands/poblar_productos.py

python manage.py poblar_productos
```

### Limpiar Productos Sin Stock

```bash
# Desde shell
python manage.py shell
>>> from productos.models import Producto
>>> Producto.objects.filter(stock=0, vendidos=0).delete()
```

---

## 📚 Recursos Adicionales

### Documentación del Proyecto

```bash
# Ver documentación de mejoras
cat docs/MEJORAS_IMPLEMENTADAS.md

# Ver plan de mejoras
cat docs/PLAN_MEJORAS_DETALLE.md

# Ver guía de pruebas
cat docs/GUIA_PRUEBAS.md

# Ver resumen ejecutivo
cat docs/RESUMEN_EJECUTIVO.md
```

---

## ⚡ Comandos Rápidos (Cheatsheet)

```bash
# Activar venv
source .venv/bin/activate

# Servidor
python manage.py runserver

# Migraciones
python manage.py makemigrations && python manage.py migrate

# Superusuario
python manage.py createsuperuser

# Shell
python manage.py shell

# Tests
python manage.py test

# Collectstatic
python manage.py collectstatic --noinput

# Check
python manage.py check --deploy
```

---

**💡 Tip:** Guarda este archivo en tus marcadores para acceso rápido a comandos comunes.
