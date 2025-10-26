# 🎨 GUÍA COMPLETA DE FRONTEND Y DISEÑO - LUST MARKETPLACE

**Fecha de creación:** 26 de Octubre, 2025  
**Versión:** 1.0  
**Para:** Sara (Frontend Developer)  
**Proyecto:** LUST MarketPlace - E-commerce con tema Anime/Neón

---

## 📑 ÍNDICE

1. [Información General del Proyecto](#información-general-del-proyecto)
2. [Estructura de Archivos](#estructura-de-archivos)
3. [Ubicación de Archivos de Diseño](#ubicación-de-archivos-de-diseño)
4. [Guía de Estilos y Colores](#guía-de-estilos-y-colores)
5. [Cómo Agregar Productos](#cómo-agregar-productos)
6. [Guía de Base de Datos](#guía-de-base-de-datos)
7. [Páginas y Componentes](#páginas-y-componentes)
8. [Promociones y Banners](#promociones-y-banners)

---

## 📖 INFORMACIÓN GENERAL DEL PROYECTO

### ¿Qué es LUST MarketPlace?

LUST MarketPlace es una plataforma de e-commerce con diseño moderno inspirado en estética anime/neón. Utiliza Django como backend y HTML/CSS/JavaScript para el frontend.

### Características Principales:

- ✅ **Sistema de Usuarios:** Registro, login, perfil
- ✅ **Catálogo de Productos:** Con categorías, filtros y búsqueda
- ✅ **Carrito de Compras:** Gestión completa de items
- ✅ **Sistema de Favoritos:** Los usuarios pueden guardar productos
- ✅ **Promociones:** Banners hero, secundarios y de categoría
- ✅ **Reseñas:** Los usuarios pueden calificar productos
- ✅ **Panel Admin:** Gestión completa de productos
- ✅ **Responsive:** Adaptable a móviles y tablets

### Tema Visual:

- **Paleta de colores:** Naranja (#ff6b35) y Morado (#8b5cf6)
- **Estilo:** Anime moderno con efectos neón
- **Tipografía:** Inter (Google Fonts)
- **Efectos:** Gradientes, sombras neón, animaciones suaves

---

## 📁 ESTRUCTURA DE ARCHIVOS

```
MarketPlace LUST/
│
├── 📂 templates/                    # PLANTILLAS HTML
│   ├── base_hentai_modern.html     # ⭐ PLANTILLA BASE (TODO HEREDA DE AQUÍ)
│   │
│   ├── 📂 productos/
│   │   ├── lista_hentai_modern.html      # Página principal (catálogo)
│   │   ├── detalle.html                  # Detalle de producto
│   │   ├── carrito_modern.html           # Carrito de compras
│   │   ├── proceso_pago_modern.html      # Página de checkout
│   │   ├── pago_exitoso.html             # Confirmación de compra
│   │   │
│   │   └── 📂 admin/
│   │       ├── admin_productos.html      # Panel de administración
│   │       ├── crear_producto.html       # Formulario nuevo producto
│   │       └── editar_producto.html      # Formulario editar producto
│   │
│   └── 📂 authentication/
│       ├── login_modern.html             # Página de login
│       ├── registro_modern.html          # Página de registro
│       ├── perfil_modern.html            # Perfil de usuario
│       ├── mis_pedidos.html              # Historial de pedidos
│       ├── mis_favoritos.html            # Lista de favoritos
│       ├── mis_direcciones.html          # Direcciones de envío
│       └── editar_perfil.html            # Editar información personal
│
├── 📂 static/                       # ARCHIVOS ESTÁTICOS
│   ├── 📂 css/
│   │   ├── estilos.css                   # Estilos globales
│   │   └── 📂 themes/
│   │       └── naranja-morado.css        # ⭐ TEMA PRINCIPAL
│   │
│   ├── 📂 js/
│   │   ├── google-auth.js                # Autenticación con Google
│   │   └── chatbot.js.bak                # (Desactivado)
│   │
│   └── 📂 img/                           # Imágenes estáticas
│
├── 📂 media/                        # ARCHIVOS SUBIDOS
│   └── 📂 productos/
│       ├── [imágenes de productos]
│       └── 📂 adicionales/
│
├── 📂 productos/                    # APP PRINCIPAL
│   ├── models.py                         # ⭐ MODELOS DE BASE DE DATOS
│   ├── views.py                          # Lógica de negocio
│   ├── urls.py                           # Rutas URL
│   ├── admin.py                          # Configuración del admin
│   └── serializers.py                    # API serializers
│
├── 📂 authentication/               # APP DE AUTENTICACIÓN
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── 📂 Carrito/                      # APP DE CARRITO
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
└── 📂 payments/                     # APP DE PAGOS
    ├── models.py
    ├── views.py
    └── urls.py
```

---

## 🎨 UBICACIÓN DE ARCHIVOS DE DISEÑO

### 📍 **PLANTILLA BASE (base_hentai_modern.html)**

**Ruta:** `templates/base_hentai_modern.html`

**¿Qué contiene?**
- ✅ Header con navegación
- ✅ Footer
- ✅ Estilos CSS globales
- ✅ Scripts JavaScript
- ✅ Configuración de Tailwind CSS
- ✅ Animaciones y efectos

**Bloques disponibles para otras páginas:**
```html
{% block title %}{% endblock %}        <!-- Título de la página -->
{% block extra_css %}{% endblock %}    <!-- CSS adicional -->
{% block content %}{% endblock %}      <!-- Contenido principal -->
{% block extra_js %}{% endblock %}     <!-- JavaScript adicional -->
```

### 📍 **ESTILOS CSS**

#### 1. **Archivo Principal de Estilos**
**Ruta:** `static/css/estilos.css`
- Estilos globales
- Utilidades comunes
- Reset CSS

#### 2. **Tema Naranja-Morado**
**Ruta:** `static/css/themes/naranja-morado.css`
- ⭐ **ARCHIVO PRINCIPAL DE COLORES**
- Variables CSS personalizadas
- Paleta de colores del tema

**Variables importantes:**
```css
:root {
    --neon-orange: #ff6b35;
    --neon-purple: #8b5cf6;
    --neon-purple-light: #c4b5fd;
    --dark-bg: #1a0f1f;
    --dark-card: #2d1b69;
}
```

### 📍 **COMPONENTES DE DISEÑO**

#### **Header/Navegación**
- **Ubicación:** `templates/base_hentai_modern.html` (líneas ~200-400)
- **Elementos:**
  - Logo "LUST"
  - Menú de navegación
  - Buscador
  - Iconos de carrito y usuario
  - Botones de login/registro

#### **Footer**
- **Ubicación:** `templates/base_hentai_modern.html` (líneas ~500-700)
- **Elementos:**
  - Links útiles
  - Redes sociales
  - Copyright
  - Información de contacto

#### **Tarjetas de Producto**
- **Ubicación:** `templates/productos/lista_hentai_modern.html`
- **Clases CSS principales:**
  - `.producto-card` - Contenedor principal
  - `.producto-imagen` - Imagen del producto
  - `.producto-info` - Información del producto
  - `.producto-precio` - Precio
  - `.btn-agregar-carrito` - Botón agregar al carrito

#### **Modal/Popup de Producto**
- **Ubicación:** `templates/productos/detalle.html`
- **Elementos:**
  - Galería de imágenes
  - Información detallada
  - Selector de tallas/colores
  - Botones de acción

---

## 🎨 GUÍA DE ESTILOS Y COLORES

### **Paleta de Colores Oficial**

#### **Colores Principales:**
```
🧡 Naranja Neón:  #ff6b35  (Acentos, botones principales)
💜 Morado:        #8b5cf6  (Elementos destacados)
💫 Morado Claro:  #c4b5fd  (Hover states, bordes)
```

#### **Colores de Fondo:**
```
🌑 Fondo Oscuro:     #1a0f1f
🌌 Card Oscuro:      #2d1b69
✨ Surface Oscuro:   #4c1d95
```

#### **Colores de Estado:**
```
✅ Verde (Activo):    #00ff88
⚠️ Amarillo:         #ffc107
❌ Rojo:             #dc3545
ℹ️ Azul:            #4cc9f0
```

### **Tipografía**

```css
/* Fuente principal */
font-family: 'Inter', sans-serif;

/* Tamaños */
Títulos principales:    2.5rem - 3rem
Subtítulos:            1.5rem - 2rem
Texto normal:          1rem
Texto pequeño:         0.875rem
```

### **Efectos y Animaciones**

#### **Sombras Neón:**
```css
/* Sombra naranja */
box-shadow: 0 0 20px rgba(255, 107, 53, 0.4);

/* Sombra morada */
box-shadow: 0 0 20px rgba(139, 92, 246, 0.4);

/* Sombra combinada */
box-shadow: 0 4px 20px rgba(255, 107, 53, 0.3),
            0 0 40px rgba(139, 92, 246, 0.2);
```

#### **Gradientes:**
```css
/* Gradiente principal */
background: linear-gradient(135deg, #ff6b35, #8b5cf6);

/* Gradiente de fondo */
background: linear-gradient(135deg, #1a0f1f 0%, #2d1b69 30%, #4c1d95 60%, #6d28d9 100%);
```

#### **Transiciones:**
```css
/* Transición suave estándar */
transition: all 0.3s ease;

/* Transición hover */
transition: transform 0.3s ease, box-shadow 0.3s ease;
```

### **Bordes y Radios**

```css
/* Cards */
border-radius: 20px - 24px;

/* Botones */
border-radius: 12px - 16px;

/* Botones pequeños */
border-radius: 8px - 10px;

/* Círculos (avatares, badges) */
border-radius: 50%;
```

---

## 🛍️ CÓMO AGREGAR PRODUCTOS

### **Opción 1: Panel de Administración Django (Recomendado para comenzar)**

#### **Paso 1: Acceder al Panel Admin**
1. Abre tu navegador
2. Ve a: `http://127.0.0.1:8000/admin/`
3. Inicia sesión con las credenciales de superusuario

#### **Paso 2: Agregar Producto**
1. En el panel lateral, busca **"Productos"**
2. Haz clic en **"+ Agregar"**
3. Completa los campos:

**Campos Obligatorios:**
- **Nombre:** Nombre del producto (ej: "Camiseta Anime Naruto")
- **Descripción:** Descripción detallada del producto
- **Precio:** Precio en USD (ej: 29.99)
- **Stock:** Cantidad disponible (ej: 50)
- **Categoría:** Selecciona una categoría existente
- **Imagen:** Sube la imagen principal del producto

**Campos Opcionales:**
- **Precio de Oferta:** Si el producto está en descuento
- **Imágenes adicionales:** Imagen 2, 3, 4 para galería
- **Tallas disponibles:** S,M,L,XL (separadas por comas)
- **Colores disponibles:** Rojo#FF0000,Negro#000000 (nombre#código)
- **Meta título y descripción:** Para SEO

**Checkboxes:**
- ✅ **Activo:** El producto aparecerá en la tienda
- ✅ **Destacado:** Aparecerá en la sección destacados
- ✅ **Nuevo:** Marcado como "Nuevo"
- ✅ **Más vendido:** Aparecerá en más vendidos

4. Haz clic en **"Guardar"**

#### **Paso 3: Verificar**
1. Ve a la página principal: `http://127.0.0.1:8000/`
2. El producto debería aparecer en el catálogo

---

### **Opción 2: Panel de Administración Personalizado**

#### **Acceso:**
- URL: `http://127.0.0.1:8000/admin-productos/`
- Se requiere iniciar sesión

#### **Características:**
- ✅ Interfaz moderna con tema anime
- ✅ Vista de lista con estadísticas
- ✅ Búsqueda y filtros
- ✅ Edición rápida
- ✅ Activar/desactivar productos

#### **Pasos:**
1. Haz clic en **"+ Crear Producto"**
2. Completa el formulario (similar al admin Django)
3. Sube las imágenes
4. Guarda el producto

---

### **Opción 3: Importación Masiva (Avanzado)**

Si tienes muchos productos, puedes usar un script Python:

#### **Crear archivo:** `importar_productos.py`
```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketplace_lust.settings')
django.setup()

from productos.models import Producto, Categoria

# Obtener categoría
categoria = Categoria.objects.get(nombre="Tu Categoría")

# Crear productos
productos = [
    {
        "nombre": "Producto 1",
        "descripcion": "Descripción del producto 1",
        "precio": 29.99,
        "stock": 100,
        "categoria": categoria,
        "activo": True,
        "destacado": True,
    },
    # Agregar más productos...
]

for p in productos:
    Producto.objects.create(**p)
    print(f"✅ Producto '{p['nombre']}' creado")

print("🎉 Importación completada")
```

#### **Ejecutar:**
```bash
python importar_productos.py
```

---

## 🗄️ GUÍA DE BASE DE DATOS

### **¿Qué es la Base de Datos?**

La base de datos es donde se almacena toda la información del marketplace:
- Productos
- Usuarios
- Pedidos
- Carritos
- Favoritos
- Reseñas
- etc.

### **Archivo de Base de Datos:**
- **Ubicación:** `db.sqlite3`
- **Tipo:** SQLite (archivo único)
- **Tamaño:** Crece con los datos

### **Modelos Principales:**

#### **1. Producto (`productos.models.Producto`)**

**Campos importantes:**
```python
nombre              # Nombre del producto
descripcion         # Descripción completa
precio              # Precio regular
precio_oferta       # Precio en oferta (opcional)
stock               # Cantidad disponible
categoria           # Categoría del producto
imagen              # Imagen principal
imagen_2, 3, 4      # Imágenes adicionales
activo              # ¿Está visible en la tienda?
destacado           # ¿Es un producto destacado?
nuevo               # ¿Es nuevo?
mas_vendido         # ¿Es más vendido?
vendidos            # Cantidad vendida
fecha_creacion      # Cuándo se creó
```

**Relaciones:**
- Pertenece a una `Categoría`
- Tiene muchas `ImagenProducto` (galería)
- Tiene muchas `Resena` (reseñas)
- Puede estar en `Favorito`
- Puede estar en `Promocion`

#### **2. Categoría (`productos.models.Categoria`)**

**Campos:**
```python
nombre              # Nombre de la categoría
slug                # URL amigable
descripcion         # Descripción
imagen              # Imagen de portada
activa              # ¿Está activa?
```

**Relación:**
- Tiene muchos `Producto`

#### **3. Orden (`productos.models.Orden`)**

**Campos:**
```python
usuario             # Usuario que compró
numero_orden        # Número único de orden
total               # Total a pagar
estado              # Estado del pedido
metodo_pago         # Cómo se pagó
direccion_envio     # Dónde enviar
```

**Estados posibles:**
- `pendiente` - Recién creada
- `procesando` - En preparación
- `enviado` - En camino
- `entregado` - Completada
- `cancelado` - Cancelada

#### **4. Promocion (`productos.models.Promocion`)**

**Campos:**
```python
titulo              # Título de la promoción
tipo                # banner, descuento, bundle
posicion            # hero, secundaria, categoria
imagen_principal    # Banner grande
descuento_porcentaje # % de descuento
fecha_inicio        # Cuándo comienza
fecha_fin           # Cuándo termina
activa              # ¿Está activa?
```

### **Comandos Útiles de Base de Datos:**

#### **Ver datos en la base de datos:**
```bash
python manage.py dbshell
```

#### **Crear backup:**
```bash
# Windows
copy db.sqlite3 backups\backup_%date%.sqlite3

# Linux/Mac
cp db.sqlite3 backups/backup_$(date +%Y%m%d).sqlite3
```

#### **Restaurar backup:**
```bash
# Windows
copy backups\backup_FECHA.sqlite3 db.sqlite3

# Linux/Mac
cp backups/backup_FECHA.sqlite3 db.sqlite3
```

#### **Resetear base de datos (¡CUIDADO! Borra todo):**
```bash
# Borrar base de datos
del db.sqlite3  # Windows
rm db.sqlite3   # Linux/Mac

# Recrear
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser
```

### **Explorar la Base de Datos (Herramientas):**

#### **Opción 1: DB Browser for SQLite (Recomendado)**
1. Descarga: https://sqlitebrowser.org/
2. Abre `db.sqlite3`
3. Puedes ver y editar tablas

#### **Opción 2: Usando Python:**
```python
python manage.py shell

>>> from productos.models import Producto
>>> Producto.objects.all()  # Ver todos los productos
>>> Producto.objects.filter(destacado=True)  # Solo destacados
>>> Producto.objects.get(id=1)  # Producto específico
```

---

## 📄 PÁGINAS Y COMPONENTES

### **1. Página Principal (Home)**

**Archivo:** `templates/productos/lista_hentai_modern.html`

**Secciones:**
- 🎯 **Hero Banner:** Carrusel de promociones principales
- ⭐ **Productos Destacados:** Grid de productos destacados
- 🆕 **Nuevos Productos:** Últimos agregados
- 💎 **Más Vendidos:** Productos populares
- 🏷️ **Categorías:** Grid de categorías
- 📣 **Promociones Secundarias:** Banners adicionales

**Estilos a modificar:**
```html
<!-- Hero Banner -->
<section class="hero-section">
  <!-- Carrusel aquí -->
</section>

<!-- Grid de Productos -->
<section class="productos-grid">
  <div class="producto-card">
    <!-- Card de producto -->
  </div>
</section>
```

**Clases CSS importantes:**
- `.hero-slide` - Slide del banner
- `.producto-card` - Card de producto
- `.producto-imagen-container` - Contenedor de imagen
- `.producto-badge` - Badge "Nuevo", "Destacado"
- `.producto-precio` - Precio del producto
- `.btn-carrito` - Botón agregar al carrito
- `.btn-favorito` - Botón corazón

---

### **2. Detalle de Producto**

**Archivo:** `templates/productos/detalle.html`

**Secciones:**
- 🖼️ **Galería de Imágenes:** Imagen principal + miniaturas
- 📝 **Información:** Nombre, precio, descripción
- 🎨 **Variantes:** Selector de tallas y colores
- 🛒 **Acciones:** Agregar al carrito, favoritos
- ⭐ **Reseñas:** Lista de reviews de usuarios
- 💡 **Productos Relacionados:** Sugerencias

**Elementos para diseñar:**
- Galería de imágenes con zoom
- Selector de cantidad
- Selector de tallas (si aplica)
- Selector de colores (si aplica)
- Área de reviews
- Formulario para dejar review

---

### **3. Carrito de Compras**

**Archivo:** `templates/productos/carrito_modern.html`

**Secciones:**
- 📦 **Lista de Items:** Productos en el carrito
- 🔢 **Cantidad:** Selector de cantidad por item
- 💰 **Resumen:** Subtotal, envío, total
- 🗑️ **Acciones:** Eliminar item, actualizar cantidad
- ➡️ **Checkout:** Botón proceder al pago

**Clases CSS:**
- `.carrito-item` - Item del carrito
- `.carrito-imagen` - Imagen del producto
- `.carrito-info` - Información del producto
- `.carrito-cantidad` - Selector de cantidad
- `.carrito-subtotal` - Subtotal del item
- `.carrito-resumen` - Resumen de compra

---

### **4. Proceso de Pago (Checkout)**

**Archivo:** `templates/productos/proceso_pago_modern.html`

**Secciones:**
1. **Información de Envío**
   - Dirección de entrega
   - Datos de contacto

2. **Método de Pago**
   - Tarjeta
   - Transferencia
   - Efectivo

3. **Resumen de Orden**
   - Items
   - Total

4. **Confirmación**
   - Botón finalizar compra

---

### **5. Perfil de Usuario**

**Archivo:** `templates/authentication/perfil_modern.html`

**Secciones:**
- 👤 **Información Personal:** Nombre, email, teléfono
- 📦 **Mis Pedidos:** Historial de compras
- ❤️ **Mis Favoritos:** Productos guardados
- 📍 **Mis Direcciones:** Direcciones de envío
- ⚙️ **Configuración:** Cambiar contraseña

---

### **6. Panel de Administración**

**Archivo:** `templates/productos/admin/admin_productos.html`

**Secciones:**
- 📊 **Estadísticas:** Total productos, activos, inactivos
- 📋 **Lista de Productos:** Tabla con todos los productos
- ➕ **Crear Producto:** Botón para nuevo producto
- ✏️ **Editar:** Link para editar cada producto
- 🗑️ **Desactivar:** Botón para desactivar producto

**Formularios:**
- `crear_producto.html` - Crear nuevo
- `editar_producto.html` - Editar existente

---

## 🎁 PROMOCIONES Y BANNERS

### **¿Qué son las Promociones?**

Las promociones son banners especiales que aparecen en la página principal para destacar ofertas, descuentos o productos especiales.

### **Tipos de Promociones:**

#### **1. Hero (Banner Principal)**
- **Posición:** Top de la página principal
- **Tamaño:** Grande, full width
- **Cantidad:** Hasta 5 slides en carrusel
- **Uso:** Ofertas principales, lanzamientos

#### **2. Secundaria**
- **Posición:** Entre secciones de productos
- **Tamaño:** Mediano
- **Cantidad:** 2-4 banners
- **Uso:** Categorías destacadas, descuentos

#### **3. Categoría**
- **Posición:** Dentro de listado de categoría
- **Tamaño:** Pequeño/Mediano
- **Uso:** Promociones específicas de categoría

### **Cómo Crear una Promoción:**

#### **Panel Admin Django:**

1. Ve a: `http://127.0.0.1:8000/admin/`
2. Busca **"Promociones"**
3. Clic en **"+ Agregar promoción"**

**Campos:**

```
Título: Nombre de la promoción (ej: "Oferta Navideña")
Subtítulo: Texto secundario (ej: "Hasta 50% de descuento")
Descripción: Detalles completos

Tipo: banner | descuento | bundle
Posición: hero | secundaria | categoria

Imagen Principal: Banner grande (recomendado 1920x600px)
Imagen Mobile: Banner para móviles (opcional, 800x400px)

Productos: Selecciona productos incluidos
Categoría: O selecciona categoría completa

Descuento (%): Porcentaje de descuento (si aplica)
Precio Especial: Precio fijo (si aplica)

URL Personalizada: Link al hacer clic (opcional)
Texto del Botón: Texto del CTA (ej: "Comprar Ahora")

Fecha Inicio: Cuándo empieza la promo
Fecha Fin: Cuándo termina

Orden: Número de orden en el carrusel (menor = primero)
Activa: ✅ Marcar para que aparezca

Estilo:
- Color Primary: Color principal (#ff6b35)
- Color Secondary: Color secundario (#8b5cf6)
- Efecto Glow: Efecto de brillo
- Tipo de Animación: Estilo de animación
```

4. Guardar

**Recomendaciones de Imágenes:**
- **Hero:** 1920x600px (mínimo)
- **Secundaria:** 1200x400px
- **Mobile:** 800x400px
- **Formato:** JPG o PNG
- **Peso:** Máximo 500KB

---

## 🔧 COMANDOS ÚTILES

### **Iniciar Servidor:**
```bash
# Activar entorno virtual
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Iniciar servidor
python manage.py runserver
```

### **Ver en el navegador:**
```
http://127.0.0.1:8000/
```

### **Rutas Importantes:**
```
/                           → Página principal
/producto/1/                → Detalle de producto (ID 1)
/carrito/                   → Carrito de compras
/pago/                      → Proceso de pago
/login/                     → Iniciar sesión
/register/                  → Registro
/perfil/                    → Perfil de usuario
/admin/                     → Panel admin Django
/admin-productos/           → Panel admin personalizado
```

---

## 📝 NOTAS IMPORTANTES PARA FRONTEND

### **Al Modificar Estilos:**

1. ✅ **Siempre edita:** `templates/base_hentai_modern.html`
2. ✅ **Mantén la paleta de colores** naranja-morado
3. ✅ **Usa las clases de Tailwind** ya configuradas
4. ✅ **Prueba en responsive** (móvil, tablet, desktop)

### **Al Agregar Imágenes:**

1. ✅ **Productos:** Sube vía admin
2. ✅ **Estáticas:** Coloca en `static/img/`
3. ✅ **Optimiza el peso** (máx 500KB)
4. ✅ **Usa WebP** para mejor rendimiento

### **Recursos Externos Usados:**

- **Tailwind CSS:** https://cdn.tailwindcss.com
- **DaisyUI:** https://cdn.jsdelivr.net/npm/daisyui
- **Font Awesome:** https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0
- **Google Fonts:** Inter
- **GSAP:** Animaciones
- **AOS:** Scroll animations

---

## 🆘 SOLUCIÓN DE PROBLEMAS

### **Los estilos no se aplican:**
1. Refresca con `Ctrl + F5` (hard refresh)
2. Verifica que el servidor esté corriendo
3. Revisa la consola del navegador (F12)

### **Las imágenes no aparecen:**
1. Verifica que estén en `media/productos/`
2. Comprueba que `MEDIA_URL` y `MEDIA_ROOT` estén configurados
3. Asegúrate que el producto tenga `imagen` asignada

### **No puedo acceder al admin:**
1. Crea un superusuario:
   ```bash
   python manage.py createsuperuser
   ```
2. Usa esas credenciales en `/admin/`

---

## 📞 CONTACTO Y SOPORTE

**Desarrollador Backend:** [Tu nombre]
**Frontend Developer:** Sara
**Proyecto:** LUST MarketPlace

---

**¡Listo para diseñar! 🎨✨**

Esta guía será actualizada conforme el proyecto evolucione.

---

*Última actualización: 26 de Octubre, 2025*
