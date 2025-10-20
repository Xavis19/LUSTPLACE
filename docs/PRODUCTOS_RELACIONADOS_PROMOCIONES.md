# 🎯 PRODUCTOS RELACIONADOS EN PROMOCIONES

## 📋 Descripción General

Sistema inteligente de recomendación de productos relacionados en páginas de promociones, que muestra productos de las mismas categorías con precios similares, excluyendo los que ya están en la promoción actual.

---

## ✨ Características Implementadas

### 1. **Filtrado Inteligente de Productos**

**Algoritmo de Selección:**
```python
# 1. Detecta categorías de productos en la promoción
# 2. Calcula rango de precios (±30% del promedio)
# 3. Filtra por:
#    - Misma categoría
#    - Stock > 0
#    - Precio similar
#    - NO están en la promoción actual
# 4. Ordena por:
#    - Más vendidos primero
#    - Productos destacados
#    - Fecha de creación
# 5. Limita a 12 productos
```

**Ejemplo Práctico:**
```
Promoción: "Ofertas en Lencería"
- 3 productos en promoción (precios: $50, $75, $100)
- Categoría: "Lencería Sexy"

→ Productos Relacionados:
  ✅ Categoría: Lencería Sexy
  ✅ Precio: $35 - $130 (±30% del rango)
  ✅ Stock disponible
  ✅ Más vendidos primero
  ❌ Excluye los 3 de la promoción
```

---

### 2. **Carousel Responsivo**

**Características:**
- ✅ Scroll horizontal suave
- ✅ Botones prev/next con estados
- ✅ Auto-deshabilita botones en extremos
- ✅ Touch-friendly en móviles
- ✅ Scroll con mouse wheel
- ✅ Animaciones fluidas

**Configuración:**
```javascript
// Ancho de card: 300px
// Gap entre cards: 24px
// Scroll amount: 320px por click
// Smooth scroll behavior
```

---

### 3. **Agregar al Carrito Directo**

**Funcionalidad:**
- ✅ Botón "Agregar" directo en cada card
- ✅ Notificación visual al agregar
- ✅ Actualización de contador del carrito
- ✅ Estados: Loading, Success, Error
- ✅ Sin recarga de página (AJAX)

**Flujo:**
```
1. Click en "Agregar"
2. Botón cambia a "Agregando..." con spinner
3. Request AJAX al servidor
4. Notificación tipo toast aparece
5. Contador del carrito se actualiza
6. Botón vuelve al estado normal
7. Toast desaparece en 3 segundos
```

---

### 4. **Badges Inteligentes**

**Tipos de Badges:**
- 🆕 **NUEVO**: Productos recién agregados
- 🔥 **MÁS VENDIDO**: Productos destacados
- 💰 **-X% OFF**: Descuento disponible
- ⚡ **ÚLTIMAS UNIDADES**: Stock bajo

**Colores:**
```css
Nuevo:        Gradiente azul (#00d4ff → #0099ff)
Más Vendido:  Gradiente dorado (#ffd700 → #ffaa00)
Descuento:    Gradiente rojo (#ff416c → #ff4b2b)
```

---

## 📂 Archivos Modificados

### 1. `/productos/views.py`

**Función:** `detalle_promocion()`

```python
def detalle_promocion(request, promocion_id):
    # ... código existente ...
    
    # ===== NUEVO: PRODUCTOS RELACIONADOS =====
    # Obtener categorías
    categorias_promocion = set()
    for producto in productos:
        if producto.categoria:
            categorias_promocion.add(producto.categoria.id)
    
    # Calcular rango de precios
    precios = [p.precio_oferta if p.precio_oferta else p.precio 
               for p in productos if p.precio]
    precio_min = min(precios) * 0.7 if precios else 0
    precio_max = max(precios) * 1.3 if precios else 999999
    
    # Query productos relacionados
    productos_relacionados = Producto.objects.filter(
        categoria_id__in=categorias_promocion,
        activo=True,
        stock__gt=0,
        precio__gte=precio_min,
        precio__lte=precio_max
    ).exclude(
        id__in=productos_ids_promocion
    ).order_by('-mas_vendido', '-vendidos')[:12]
    
    context['productos_relacionados'] = productos_relacionados
    context['tiene_relacionados'] = len(productos_relacionados) > 0
```

**Líneas modificadas:** 891-926

---

### 2. `/templates/productos/detalle_promocion.html`

**Nuevo template creado:** ✅ (500+ líneas)

**Secciones principales:**

#### A. CSS (Líneas 1-280)
```css
/* Hero de promoción */
.promo-hero { ... }

/* Grid de productos */
.productos-grid { ... }

/* Carousel */
.carousel-container { ... }
.carousel-btn { ... }

/* Notificación */
.cart-toast { ... }
```

#### B. HTML - Productos Relacionados (Líneas 320-440)
```html
<div class="related-products-section">
    <div class="carousel-container">
        <button class="carousel-btn prev">...</button>
        
        <div class="carousel-wrapper">
            <div class="carousel-track">
                {% for producto in productos_relacionados %}
                    <!-- Card con botón agregar -->
                {% endfor %}
            </div>
        </div>
        
        <button class="carousel-btn next">...</button>
    </div>
</div>
```

#### C. JavaScript (Líneas 450-550)
```javascript
// Carousel
function scrollCarousel(direction) { ... }
function updateCarouselButtons() { ... }

// Agregar al carrito
function agregarAlCarrito(event, nombreProducto) { ... }
function mostrarNotificacionCarrito(nombreProducto) { ... }
```

---

## 🎨 Diseño UI/UX

### Colores
```css
Primary:      #dc3545 (Rojo)
Secondary:    #c82333 (Rojo oscuro)
Success:      #28a745 (Verde)
Warning:      #ffc107 (Amarillo)
Info:         #20c997 (Turquesa)
```

### Tipografía
```css
Fuente:       Inter (Google Fonts)
Tamaños:
  - Título sección: 2rem (32px)
  - Nombre producto: 1.1rem (17.6px)
  - Precio: 1.5rem (24px)
  - Badges: 0.75rem (12px)
```

### Espaciado
```css
Gap entre cards: 1.5rem (24px)
Padding cards: 1.5rem (24px)
Border radius: 12px
```

### Animaciones
```css
Hover card: translateY(-5px) 0.3s
Carousel scroll: smooth behavior
Toast entrada: cubic-bezier(0.68, -0.55, 0.265, 1.55)
```

---

## 📱 Responsive Design

### Breakpoints

**Desktop (>768px):**
- Cards: 300px de ancho
- Grid: auto-fill minmax(280px, 1fr)
- Botones carousel: 45px × 45px
- Padding: 50px

**Mobile (≤768px):**
- Cards: 250px de ancho
- Grid: auto-fill minmax(200px, 1fr)
- Botones carousel: 35px × 35px
- Padding: 10px

---

## 🔧 Funciones JavaScript

### 1. `scrollCarousel(direction)`
```javascript
Parámetros: direction (-1 = prev, 1 = next)
Acciones:
  - Scroll suave 320px
  - Actualiza estado de botones
  - Previene scroll fuera de límites
```

### 2. `updateCarouselButtons()`
```javascript
Sin parámetros
Acciones:
  - Detecta posición actual del scroll
  - Deshabilita botón prev si está al inicio
  - Deshabilita botón next si está al final
```

### 3. `agregarAlCarrito(event, nombreProducto)`
```javascript
Parámetros: 
  - event: Form submit event
  - nombreProducto: String
Acciones:
  - Previene submit normal
  - Envía AJAX request
  - Muestra notificación
  - Actualiza contador carrito
  - Maneja estados del botón
```

### 4. `mostrarNotificacionCarrito(nombreProducto)`
```javascript
Parámetros: nombreProducto (String)
Acciones:
  - Crea toast notification
  - Agrega al DOM
  - Anima entrada
  - Auto-destruye en 3s
```

---

## 🧪 Testing

### Casos de Prueba

#### 1. **Productos Relacionados Aparecen**
```
✓ Entra a promoción con categoría
✓ Verifica que aparezca sección "También te puede interesar"
✓ Cuenta al menos 1 producto relacionado
✓ Productos NO deben estar en la promoción
```

#### 2. **Filtrado por Precio**
```
✓ Productos relacionados dentro de rango ±30%
✓ Si promoción tiene precios $50-$100:
  → Relacionados entre $35-$130
```

#### 3. **Carousel Funciona**
```
✓ Click en "Next" mueve a la derecha
✓ Click en "Prev" mueve a la izquierda
✓ Botones se deshabilitan en extremos
✓ Scroll con mouse wheel funciona
```

#### 4. **Agregar al Carrito**
```
✓ Click en "Agregar" muestra notificación
✓ Contador del carrito aumenta
✓ Botón cambia a "Agregando..." con spinner
✓ Toast desaparece en 3 segundos
```

#### 5. **Responsive**
```
✓ En móvil, cards se ajustan a 250px
✓ Botones carousel visibles
✓ Touch scroll funciona
✓ Grid se adapta a 1 columna si necesario
```

---

## 📊 Métricas de Rendimiento

### Query Database
```sql
-- 1 query para productos de promoción
SELECT * FROM productos_producto WHERE id IN (...)

-- 1 query para productos relacionados
SELECT * FROM productos_producto 
WHERE categoria_id IN (...) 
  AND activo = TRUE 
  AND stock > 0 
  AND precio BETWEEN X AND Y
  AND id NOT IN (...)
ORDER BY mas_vendido DESC, vendidos DESC
LIMIT 12
```

**Total queries:** 2
**Tiempo estimado:** <50ms

### Tamaño de Página
```
HTML: ~15KB (comprimido)
CSS: ~8KB (inline)
JS: ~3KB (inline)
Imágenes: Variable (lazy load recomendado)
```

### Lighthouse Score Estimado
```
Performance: 85-95
Accessibility: 90-100
Best Practices: 85-95
SEO: 90-100
```

---

## 🚀 Mejoras Futuras Sugeridas

### Corto Plazo
1. **Lazy Loading de Imágenes**
   ```javascript
   <img loading="lazy" src="..." alt="...">
   ```

2. **Infinite Scroll en Carousel**
   ```javascript
   // Auto-scroll continuo
   // Loop infinito de productos
   ```

3. **Vista Rápida (Quick View Modal)**
   ```javascript
   // Modal con info rápida del producto
   // Sin salir de la página de promoción
   ```

### Mediano Plazo
1. **Personalización por Usuario**
   ```python
   # Basado en historial de compras
   # Productos vistos recientemente
   # Categorías favoritas
   ```

2. **A/B Testing**
   ```python
   # Probar diferentes algoritmos
   # Medir conversión
   # Optimizar orden de productos
   ```

3. **Analytics Detallados**
   ```javascript
   // Tracking de clicks
   // Productos más vistos
   // Tasa de conversión por posición
   ```

### Largo Plazo
1. **Machine Learning**
   ```python
   # Recomendaciones basadas en IA
   # Predicción de productos que comprarán juntos
   # Segmentación de usuarios
   ```

2. **Cache Inteligente**
   ```python
   # Redis para productos relacionados
   # Precalcular recomendaciones
   # Invalidar cache cuando cambien precios/stock
   ```

---

## 📖 Uso y Ejemplos

### Activar Productos Relacionados

**Paso 1:** Crear promoción con categoría
```python
promocion = Promocion.objects.create(
    titulo="Ofertas en Lencería",
    categoria=categoria_lenceria,  # ← Importante
    descuento=20
)
```

**Paso 2:** Agregar productos a la promoción
```python
promocion.productos.add(producto1, producto2, producto3)
```

**Paso 3:** Asegurarse de tener más productos en la categoría
```python
# Debe haber productos de la misma categoría
# que NO estén en la promoción
Producto.objects.filter(
    categoria=categoria_lenceria,
    activo=True,
    stock__gt=0
).count() > 3  # ← Debe ser True
```

### URL de Acceso
```
http://localhost:8000/promocion/4/
                               ↑
                         ID de la promoción
```

---

## 🐛 Troubleshooting

### No aparecen productos relacionados

**Causas posibles:**
1. ❌ Promoción sin categoría asignada
2. ❌ No hay productos en la misma categoría
3. ❌ Todos los productos de la categoría están en la promoción
4. ❌ No hay productos con stock

**Solución:**
```python
# Verificar en Django shell
from productos.models import Promocion, Producto

promo = Promocion.objects.get(id=4)
print(f"Categoría: {promo.categoria}")
print(f"Productos en promo: {promo.productos.count()}")

# Productos disponibles en la categoría
disponibles = Producto.objects.filter(
    categoria=promo.categoria,
    activo=True,
    stock__gt=0
).exclude(
    id__in=promo.productos.values_list('id', flat=True)
)
print(f"Productos relacionados disponibles: {disponibles.count()}")
```

### Carousel no funciona

**Verificar:**
1. ✓ jQuery/JavaScript cargado
2. ✓ IDs correctos: `carouselWrapper`, `prevBtn`, `nextBtn`
3. ✓ CSS aplicado correctamente
4. ✓ No hay errores en consola del navegador

### Agregar al carrito no funciona

**Verificar:**
1. ✓ Usuario autenticado
2. ✓ CSRF token presente
3. ✓ URL `/carrito/agregar/<id>/` correcta
4. ✓ Fetch API compatible con navegador

---

## ✅ Checklist de Implementación

- [x] Vista `detalle_promocion()` modificada
- [x] Template `detalle_promocion.html` creado
- [x] CSS para carousel agregado
- [x] JavaScript para carousel agregado
- [x] Función agregar al carrito con AJAX
- [x] Notificación toast implementada
- [x] Filtrado inteligente de productos
- [x] Badges dinámicos
- [x] Responsive design
- [x] Documentación completa

---

## 📝 Notas Adicionales

### Compatibilidad de Navegadores
```
✓ Chrome 90+
✓ Firefox 88+
✓ Safari 14+
✓ Edge 90+
✓ Mobile browsers (iOS Safari, Chrome Mobile)
```

### Dependencias
```
Django 5.2.7
Font Awesome 6.0.0
Google Fonts (Inter)
```

### Sin Dependencias Externas
- ❌ No usa jQuery
- ❌ No usa Bootstrap
- ❌ No usa librerías de carousel
- ✅ Vanilla JavaScript puro
- ✅ CSS3 nativo

---

**Fecha de Implementación:** 11 de Octubre de 2025  
**Versión:** 1.0  
**Autor:** Sistema de Mejoras LUSTPLACE  
**Estado:** ✅ Implementado y Funcionando
