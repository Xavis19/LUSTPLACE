# 🔥 LUSTPLACE - Marketplace Moderno

![Django](https://img.shields.io/badge/Django-5.2.7-green?style=for-the-badge&logo=django)
![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)
![Status](https://img.shields.io/badge/Status-Activo-brightgreen?style=for-the-badge)

**LUSTPLACE** es un marketplace moderno desarrollado en Django con un diseño visual impactante, sistema de autenticación completo, carrito de compras inteligente y panel administrativo avanzado.

## � Características Principales

### ✨ **Interfaz Moderna**
- 🎨 Diseño hentai/anime con gradientes naranja-morado
- 🌟 Partículas animadas flotantes (emojis temáticos)
- 📱 Totalmente responsive (móvil, tablet, desktop)
- 🎭 Efectos hover y transiciones suaves
- �️ Fondo fijo que se mantiene al hacer scroll

### 🛒 **Sistema de E-commerce**
- 🛍️ Catálogo de productos con filtrado AJAX
- ❤️ Sistema de favoritos por usuario
- 🛒 Carrito de compras inteligente
- 💰 Gestión de precios y ofertas
- 📦 Control de inventario/stock
- 🏷️ Sistema de categorías

### 🔐 **Autenticación y Usuarios**
- 👤 Registro y login completo
- � Autenticación JWT
- 📝 Perfiles de usuario editables
- 📍 Gestión de direcciones
- 📋 Historial de pedidos
- ❤️ Lista de favoritos personalizada

### ⚡ **Panel Administrativo**
- 🎛️ Control total de productos
- 📊 Gestión de promociones (activar/desactivar)
- 👥 Administración de usuarios
- 📈 Acciones masivas optimizadas
- 📋 Filtros y búsquedas avanzadas
---

## �️ Arquitectura del Proyecto

```
LUSTPLACE/
├── 🎯 marketplace_lust/     # Configuración principal Django
├── 👤 authentication/      # Sistema completo de usuarios
├── 🛍️ productos/          # Catálogo y gestión de productos  
├── 🛒 Carrito/            # Sistema de carrito de compras
├── 💳 payments/           # Procesamiento de pagos
├── 🥽 VirtualR/           # Funcionalidades de realidad virtual
├── 🔑 login/             # Autenticación adicional
├── 🎨 templates/         # Plantillas HTML organizadas
├── 🖼️ static/           # Archivos CSS, JS e imágenes
├── 📁 media/            # Archivos subidos (avatares, productos)
└── 📚 docs/             # Documentación del proyecto
```

---

## 📚 Documentación de las Apps

### 🎯 **marketplace_lust** (Configuración Principal)
**Ubicación:** `/marketplace_lust/`

**Función:** Núcleo del proyecto Django con todas las configuraciones.

#### � Archivos principales:
- **`settings.py`** - Configuración completa del proyecto
- **`urls.py`** - Ruteo principal de URLs 
- **`wsgi.py/asgi.py`** - Configuración para despliegue

#### 🔧 **Configuraciones modificables:**
```python
# Base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Cambiar a PostgreSQL
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Idioma y zona horaria
LANGUAGE_CODE = 'es'  # Español por defecto
TIME_ZONE = 'America/Bogota'  # Ajustar según ubicación

# Configuración de archivos media
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

---

### 👤 **authentication** (Sistema de Usuarios)
**Ubicación:** `/authentication/`

**Función:** Gestión completa de usuarios, perfiles, direcciones y favoritos.

#### 🗂️ **Modelos principales:**
- **`UserProfile`** - Perfil extendido del usuario
- **`Direccion`** - Direcciones de entrega del usuario  
- **`Favorito`** - Productos favoritos por usuario
- **`Factura`** - Sistema de facturación

#### 🎨 **Templates disponibles:**
- `perfil_usuario.html` - Vista del perfil
- `editar_perfil.html` - Formulario de edición
- `mis_direcciones.html` - Gestión de direcciones
- `mis_favoritos.html` - Lista de productos favoritos
- `mis_pedidos.html` - Historial de compras

#### � **Personalización posible:**
```python
# En models.py - Agregar campos al perfil
class UserProfile(models.Model):
    telefono = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField(null=True)
    # Agregar más campos según necesidad
```

---

### 🛍️ **productos** (Catálogo E-commerce)
**Ubicación:** `/productos/`

**Función:** Núcleo del e-commerce con productos, categorías y promociones.

#### 🗂️ **Modelos principales:**
- **`Categoria`** - Categorías de productos
- **`Producto`** - Productos del marketplace
- **`Promocion`** - Sistema de promociones administrables

#### 🎨 **Templates principales:**
- `lista_hentai_modern.html` - Catálogo principal con filtros AJAX
- `productos_promocion.html` - Productos en promoción
- `perfil_modern.html` - Perfil de usuario moderno
- `carrito_modern.html` - Vista del carrito
- `proceso_pago_modern.html` - Checkout de pagos

#### ⚡ **Características técnicas:**
- **Filtrado AJAX** - Sin recargar página
- **Búsqueda en tiempo real** - Con debounce optimizado
- **Paginación dinámica** - Carga incremental
- **Gestión de stock** - Control automático

#### 🔧 **Configuraciones modificables:**
```python
# En models.py - Ajustar campos de producto
class Producto(models.Model):
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    precio_oferta = models.DecimalField(null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    # Agregar campos como peso, dimensiones, etc.
```

#### 🎯 **URLs principales:**
- `/` - Página principal con productos
- `/productos/` - Listado completo
- `/categoria/<id>/` - Productos por categoría
- `/producto/<id>/` - Detalle del producto
- `/filtros-ajax/` - Endpoint para filtrado AJAX

---

### 🛒 **Carrito** (Sistema de Compras)
**Ubicación:** `/Carrito/`

**Función:** Gestión del carrito de compras y proceso de checkout.

#### 🗂️ **Modelos principales:**
- **`Carrito`** - Carrito por usuario
- **`ItemCarrito`** - Productos en el carrito
- **`Pedido`** - Órdenes finalizadas

#### 🔧 **Funcionalidades personalizables:**
- Límites de cantidad por producto
- Descuentos por volumen
- Cupones de descuento
- Cálculo de envío

---

### 💳 **payments** (Procesamiento de Pagos)
**Ubicación:** `/payments/`

**Función:** Gestión de pagos y transacciones.

#### 🔧 **Integraciones posibles:**
- PayPal
- Stripe  
- Mercado Pago
- Pagos en efectivo

---

### 🥽 **VirtualR** (Realidad Virtual)
**Ubicación:** `/VirtualR/`

**Función:** Funcionalidades de realidad virtual y experiencias inmersivas.

#### 🔧 **Posibles implementaciones:**
- Vista 360° de productos
- Probadores virtuales
- Experiencias VR

---

### 🔑 **login** (Autenticación Adicional)
**Ubicación:** `/login/`

**Función:** Sistema de login complementario y autenticación social.

---

## 🎨 Sistema de Templates

### 📄 **Template Base Principal**
**Archivo:** `templates/base_hentai_modern.html`

#### 🌟 **Características:**
- **Diseño hentai/anime** con gradientes naranja-morado
- **Partículas flotantes** animadas con emojis temáticos
- **Fondo fijo** que persiste al hacer scroll
- **Responsive design** con Tailwind CSS + DaisyUI
- **Efectos visuales** modernos y atractivos

#### 🔧 **Personalización del diseño:**
```css
/* Cambiar colores del gradiente */
.hentai-bg {
    background: linear-gradient(135deg, 
        #1a0f1f 0%,    /* Negro profundo */
        #2d1b69 30%,   /* Morado oscuro */ 
        #4c1d95 60%,   /* Morado medio */
        #6d28d9 100%   /* Morado claro */
    );
}

/* Modificar partículas */
const emojiList = ['🔥', '💎', '⭐', '💫', '🌟']; // Cambiar emojis
```

### 📱 **Templates Responsivos**
Todos los templates están optimizados para:
- 📱 **Móvil** (320px - 768px)
- 📱 **Tablet** (768px - 1024px)  
- 💻 **Desktop** (1024px+)

---

## ⚙️ Instalación y Configuración

### 📋 **Prerrequisitos**
```bash
Python 3.11+
Django 5.2.7
SQLite3 (incluido) o PostgreSQL
```

### 🚀 **Instalación**
```bash
# 1. Clonar el repositorio
git clone https://github.com/Xavis19/LUSTPLACE.git
cd LUSTPLACE

# 2. Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar migraciones
python manage.py migrate

# 5. Crear superusuario
python manage.py createsuperuser

# 6. Ejecutar servidor
python manage.py runserver
```

### 🌐 **Acceso**
- **Sitio web:** http://127.0.0.1:8000/
- **Panel admin:** http://127.0.0.1:8000/admin/

---

## � Dependencias Principales

```txt
Django==5.2.7              # Framework web principal
djangorestframework==3.15.2 # API REST
Pillow==10.4.0             # Procesamiento de imágenes
psycopg2-binary==2.9.9     # Conector PostgreSQL
corsheaders==4.4.0         # Manejo de CORS
pytz==2024.2               # Zona horaria
```

---

## 🎯 Funcionalidades Destacadas

### ⚡ **AJAX Sin Recargas**
- Filtrado de productos en tiempo real
- Búsqueda instantánea con debounce
- Paginación dinámica
- Carrito que se actualiza automáticamente

### 🎨 **Efectos Visuales Avanzados**
- Partículas flotantes animadas
- Transiciones suaves entre páginas
- Efectos hover en productos
- Gradientes dinámicos

### 🔐 **Seguridad Implementada**
- Autenticación JWT
- Validación CSRF
- Sanitización de datos
- Protección contra ataques comunes

---

## 🔧 Configuraciones Avanzadas

### 🗄️ **Cambiar a PostgreSQL**
```python
# En settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'lustplace_db',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_contraseña',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 📧 **Configurar Email**
```python
# En settings.py para envío de emails
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_HOST_USER = 'tu_email@gmail.com'
EMAIL_HOST_PASSWORD = 'tu_contraseña_app'
```

### 🌐 **Configurar para Producción**
```python
# En settings.py
DEBUG = False
ALLOWED_HOSTS = ['tu-dominio.com', 'www.tu-dominio.com']
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
```

---

## 📊 Panel Administrativo

### 🎛️ **Funcionalidades Admin**
- **Productos:** CRUD completo con filtros avanzados
- **Promociones:** Activar/desactivar masivamente
- **Usuarios:** Gestión completa de perfiles
- **Pedidos:** Seguimiento y estados
- **Categorías:** Organización jerárquica

### 🔧 **Personalizar Admin**
```python
# En admin.py de cualquier app
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio', 'stock', 'activo']
    list_filter = ['categoria', 'activo', 'destacado']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['precio', 'stock', 'activo']
```

---

## 🚀 Optimizaciones Implementadas

### ⚡ **Performance**
- Consultas optimizadas con `select_related`
- Cache de queries frecuentes
- Compresión de archivos estáticos
- Lazy loading de imágenes

### � **SEO Friendly**
- URLs amigables
- Meta tags dinámicos
- Sitemap XML
- Estructura semántica HTML5

---

## 🤝 Contribución

### 📝 **Cómo contribuir**
1. Fork del repositorio
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

### 📋 **Estándares de código**
- Seguir PEP 8 para Python
- Comentarios en español
- Tests para nuevas funcionalidades
- Documentación actualizada

---

## 📞 Soporte

### 🐛 **Reportar Bugs**
- Crear issue en GitHub con:
  - Descripción del problema
  - Pasos para reproducir
  - Screenshots si es necesario
  - Información del entorno

### � **Solicitar Funcionalidades**
- Crear issue con etiqueta "enhancement"
- Descripción clara de la funcionalidad
- Casos de uso esperados

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

---

## 🌟 Créditos

**Desarrollado por:** Xavis19  
**Última actualización:** Octubre 3, 2025  
**Versión:** 2.0.0  

---

<div align="center">

**🔥 ¡LUSTPLACE - Donde la pasión se encuentra con la tecnología! 🔥**

[![GitHub](https://img.shields.io/badge/GitHub-Xavis19-black?style=for-the-badge&logo=github)](https://github.com/Xavis19)

</div>

```env
DEBUG=True
SECRET_KEY=tu_clave_secreta
DB_NAME=lustplace_db
DB_USER=lustplace_user
DB_PASSWORD=tu_password
```

## 🎨 **Stack Tecnológico**

- **Backend:** Django + DRF + PostgreSQL
- **Frontend:** Tailwind CSS + Alpine.js + GSAP
- **Autenticación:** JWT + Sessions  
- **Animaciones:** GSAP + AOS + Lottie
- **Estilos:** Glass morphism + Efectos neón

## 📈 **Próximas Características**

- [ ] Integración completa de VR
- [ ] Sistema de reseñas
- [ ] Chat en vivo
- [ ] Notificaciones push
- [ ] Análíticas avanzadas

---

**Desarrollado con 💜 para la comunidad anime/hentai**
