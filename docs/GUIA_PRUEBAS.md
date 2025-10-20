# 🧪 GUÍA DE PRUEBAS - MEJORAS EN DETALLE.HTML

## 📋 Checklist de Pruebas

### ✅ FASE 1: Verificación de Base de Datos

1. **Verificar migraciones aplicadas:**
```bash
cd /Users/editsongutierreza/Downloads/LUSTPLACE/LUSTPLACE
source .venv/bin/activate
python manage.py showmigrations productos
```

Debe mostrar:
```
[X] 0005_producto_colores_disponibles_producto_imagen_2_and_more
```

2. **Verificar campos en admin:**
- Acceder a: `http://localhost:8000/admin/productos/producto/`
- Editar cualquier producto
- Verificar que aparecen los nuevos campos:
  - imagen_2, imagen_3, imagen_4
  - vendidos
  - mas_vendido
  - colores_disponibles

3. **Verificar modelo Resena:**
- Acceder a: `http://localhost:8000/admin/productos/resena/`
- Debe aparecer la sección de Reseñas

---

### ✅ FASE 2: Pruebas Visuales

#### 1. Badges Dinámicos

**Caso 1: Badge NUEVO**
- En admin, marcar producto con `nuevo=True`
- Ir a detalle del producto
- ✅ Debe aparecer badge azul "🆕 NUEVO" en esquina superior izquierda

**Caso 2: Badge OFERTA**
- En admin, agregar `precio_oferta` menor que `precio`
- Ir a detalle
- ✅ Debe aparecer badge rojo "-X% OFF" calculado automáticamente

**Caso 3: Badge ÚLTIMAS UNIDADES**
- En admin, poner `stock=3`
- Ir a detalle
- ✅ Debe aparecer badge amarillo "⚡ ÚLTIMAS 3 UNIDADES"

**Caso 4: Badge MÁS VENDIDO**
- En admin, marcar `mas_vendido=True`
- Ir a detalle
- ✅ Debe aparecer badge rojo "🔥 MÁS VENDIDO"

#### 2. Barra de Progreso de Stock

**Configuración de prueba:**
- `stock = 30`
- `vendidos = 70`
- Total = 100, porcentaje vendido = 70%

**Resultado esperado:**
- ✅ Barra de progreso al 70%
- ✅ Texto: "🔥 70 vendidos | 📦 30 disponibles"
- ✅ Animación suave de la barra

#### 3. Selector de Colores

**Configuración de prueba:**
- `colores_disponibles = "Rojo#FF0000,Negro#000000,Rosa#FF69B4"`

**Resultado esperado:**
- ✅ 3 círculos de colores: rojo, negro, rosa
- ✅ Primer color seleccionado por defecto
- ✅ Click en color: borde rojo brillante
- ✅ Hover: escala 1.1

---

### ✅ FASE 3: Pruebas Interactivas

#### 1. Galería de Imágenes

**Configuración de prueba:**
- Subir 4 imágenes diferentes al producto
- `imagen`, `imagen_2`, `imagen_3`, `imagen_4`

**Pasos de prueba:**
1. Ir a detalle del producto
2. ✅ Deben aparecer 4 miniaturas debajo de la imagen principal
3. ✅ Primera miniatura tiene borde rojo (active)
4. Click en segunda miniatura
5. ✅ Imagen principal cambia con fade
6. ✅ Segunda miniatura ahora tiene borde rojo

#### 2. Zoom en Imagen

**Pasos de prueba:**
1. Ir a detalle del producto
2. Hover sobre imagen principal
3. ✅ Imagen hace scale(1.05)
4. Click en imagen
5. ✅ Imagen hace zoom 2x
6. ✅ Cursor cambia a zoom-out
7. Mover mouse sobre imagen
8. ✅ Zoom sigue la posición del mouse
9. Click de nuevo
10. ✅ Zoom se desactiva

#### 3. Compartir en Redes Sociales

**Pasos de prueba:**
1. Ir a detalle del producto
2. Buscar sección "Compartir:"
3. ✅ 4 botones circulares: WhatsApp, Facebook, Twitter, Link

**Prueba WhatsApp:**
- Click en botón verde
- ✅ Abre WhatsApp con mensaje pre-rellenado

**Prueba Facebook:**
- Click en botón azul
- ✅ Abre diálogo de compartir de Facebook

**Prueba Twitter:**
- Click en botón azul claro
- ✅ Abre Twitter con tweet pre-rellenado

**Prueba Copiar Enlace:**
- Click en botón gris
- ✅ Mensaje: "¡Enlace copiado al portapapeles!"
- ✅ Enlace realmente copiado (Ctrl+V para verificar)

#### 4. Notificación al Agregar al Carrito

**Pasos de prueba:**
1. Ir a detalle del producto
2. Seleccionar cantidad
3. Click en "Agregar al Carrito"
4. ✅ Botón muestra spinner: "Agregando..."
5. ✅ Notificación aparece desde arriba con animación bounce
6. ✅ Ícono verde ✅ con pulso
7. ✅ Texto: "¡Producto agregado!"
8. ✅ Botón "Ver carrito" (rojo)
9. ✅ Botón "Seguir comprando" (gris)
10. Esperar 5 segundos
11. ✅ Notificación se oculta automáticamente

**Prueba botón "Ver carrito":**
- Click en "Ver carrito"
- ✅ Redirige a `/carrito/`

**Prueba botón "Seguir comprando":**
- Click en "Seguir comprando"
- ✅ Notificación se cierra inmediatamente

---

### ✅ FASE 4: Pruebas de Admin

#### 1. Admin de Producto

**Pasos:**
1. Ir a: `http://localhost:8000/admin/productos/producto/`
2. Click en un producto para editar

**Verificar secciones:**
- ✅ "Información Básica" - nombre, descripción, categoría
- ✅ "Imágenes del Producto" - 4 campos de imagen
- ✅ "Precios y Stock" - precio, oferta, stock, vendidos
- ✅ "Variantes (Tallas y Colores)" - colapsable
- ✅ "Estados" - activo, destacado, nuevo, mas_vendido
- ✅ "SEO" - slug, meta_titulo, meta_descripcion

**Lista de productos:**
- ✅ Columnas: nombre, categoría, precio, stock, vendidos, mas_vendido

#### 2. Admin de Reseña

**Pasos:**
1. Ir a: `http://localhost:8000/admin/productos/resena/`
2. Click en "Agregar reseña"

**Verificar campos:**
- ✅ Producto (selector)
- ✅ Usuario (selector)
- ✅ Calificación (1-5 estrellas)
- ✅ Título
- ✅ Comentario
- ✅ Compra verificada (checkbox)
- ✅ Aprobado (checkbox)

**Verificar acciones:**
- Seleccionar varias reseñas
- En "Acciones":
  - ✅ "✅ Aprobar reseñas seleccionadas"
  - ✅ "❌ Rechazar reseñas seleccionadas"
  - ✅ "✓ Marcar como compra verificada"

---

### ✅ FASE 5: Pruebas Responsive

#### Desktop (> 1200px)
- ✅ Grid 2 columnas (imagen | detalles)
- ✅ Imagen a la izquierda, detalles a la derecha
- ✅ Miniaturas horizontales centradas
- ✅ Botones en fila

#### Tablet (768px - 1200px)
- ✅ Grid sigue siendo 2 columnas
- ✅ Textos se ajustan
- ✅ Padding reducido

#### Móvil (< 768px)
- ✅ Grid 1 columna (imagen arriba, detalles abajo)
- ✅ Imagen ocupa ancho completo
- ✅ Botones en columna (stack vertical)
- ✅ Features en 1 columna
- ✅ Miniaturas scroll horizontal

---

### ✅ FASE 6: Pruebas de Navegadores

#### Chrome/Edge (Chromium)
- ✅ Todas las funcionalidades
- ✅ Fetch API funciona
- ✅ Animaciones suaves

#### Firefox
- ✅ Todas las funcionalidades
- ✅ Backdrop-filter funciona
- ✅ Clipboard API funciona

#### Safari
- ✅ Todas las funcionalidades
- ✅ -webkit-backdrop-filter
- ✅ Animaciones CSS

---

### ✅ FASE 7: Pruebas de Performance

#### Tiempo de carga
- ✅ < 2 segundos carga inicial
- ✅ Imágenes lazy load (si implementado)

#### Animaciones
- ✅ 60 FPS en animaciones CSS
- ✅ No hay lag en zoom
- ✅ Transiciones suaves

#### AJAX
- ✅ Agregar al carrito < 500ms
- ✅ No recarga la página

---

## 🐛 Troubleshooting

### Problema: "No aparecen las miniaturas"
**Solución:** Verificar que el producto tenga más de 1 imagen cargada.

### Problema: "El selector de colores no aparece"
**Solución:** Verificar que `colores_disponibles` tenga el formato correcto:
```
Rojo#FF0000,Negro#000000
```

### Problema: "La notificación no aparece al agregar al carrito"
**Solución:** 
1. Verificar consola del navegador (F12)
2. Verificar que la vista de carrito acepte AJAX
3. Asegurarse de estar autenticado

### Problema: "Migración no se aplica"
**Solución:**
```bash
python manage.py makemigrations productos --name mejoras_detalle
python manage.py migrate productos
```

### Problema: "Error en porcentaje_stock_vendido"
**Solución:** Verificar que el producto tenga `vendidos > 0`

---

## ✅ Checklist Final

- [ ] Migraciones aplicadas
- [ ] Admin accesible
- [ ] Badges se muestran correctamente
- [ ] Barra de progreso funciona
- [ ] Selector de colores funciona
- [ ] Galería cambia imágenes
- [ ] Zoom funciona con mouse
- [ ] Compartir en redes abre correctamente
- [ ] Copiar enlace funciona
- [ ] Notificación aparece al agregar al carrito
- [ ] No hay errores en consola
- [ ] Responsive en móvil
- [ ] Compatible con navegadores principales

---

## 🎉 ¡Todas las pruebas pasadas = Éxito total!

**Fecha de pruebas:** __________  
**Testeado por:** __________  
**Estado:** ⬜ PENDIENTE | ⬜ EN PROCESO | ⬜ COMPLETADO
