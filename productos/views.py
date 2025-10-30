
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse  
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt  
from .models import Producto, Orden, Favorito, Promocion, PromocionView, Categoria  # ✅ IMPORTAR MODELOS NECESARIOS
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils import timezone
import json
import random

def lista_productos(request):
    """Lista de productos moderna con promociones y filtros"""
    
    # Obtener promociones activas
    promociones_hero = Promocion.objects.filter(
        activa=True,
        posicion='hero',
        fecha_inicio__lte=timezone.now(),
        fecha_fin__gte=timezone.now()
    ).order_by('orden')[:5]  # Máximo 5 slides
    
    promociones_secundarias = Promocion.objects.filter(
        activa=True,
        posicion='secundaria',
        fecha_inicio__lte=timezone.now(),
        fecha_fin__gte=timezone.now()
    ).order_by('orden')[:6]  # Máximo 6 promociones secundarias
    
    # Obtener productos con filtros
    productos = Producto.objects.filter(activo=True).select_related('categoria')
    
    # Filtros de búsqueda
    categoria_id = request.GET.get('categoria')
    precio_min = request.GET.get('precio_min')
    precio_max = request.GET.get('precio_max')
    descuento = request.GET.get('descuento')
    disponible = request.GET.get('disponible')
    ordenar = request.GET.get('ordenar', '')
    buscar = request.GET.get('q', '')
    
    # Aplicar filtros
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    
    if precio_min:
        productos = productos.filter(precio__gte=precio_min)
    
    if precio_max:
        productos = productos.filter(precio__lte=precio_max)
    
    if descuento == 'true':
        productos = productos.filter(precio_oferta__isnull=False)
    
    if disponible == 'true':
        productos = productos.filter(stock__gt=0)
    
    if buscar:
        productos = productos.filter(
            Q(nombre__icontains=buscar) | 
            Q(descripcion__icontains=buscar) |
            Q(categoria__nombre__icontains=buscar)
        )
    
    # Ordenamiento
    if ordenar == 'precio_asc':
        productos = productos.order_by('precio')
    elif ordenar == 'precio_desc':
        productos = productos.order_by('-precio')
    elif ordenar == 'nombre':
        productos = productos.order_by('nombre')
    elif ordenar == 'fecha':
        productos = productos.order_by('-fecha_creacion')
    else:
        # Por defecto: productos destacados primero, luego por fecha
        productos = productos.order_by('-destacado', '-fecha_creacion')
    
    # Paginación
    paginator = Paginator(productos, 12)  # 12 productos por página
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Obtener categorías para el filtro
    categorias = Categoria.objects.filter(activa=True).order_by('nombre')
    
    # Combinar promociones para la vista moderna
    promociones_todas = list(promociones_hero) + list(promociones_secundarias)
    
    context = {
        'productos': page_obj,
        'promociones': promociones_todas[:6],  # Máximo 6 para el grid
        'promociones_hero': promociones_hero,
        'promociones_secundarias': promociones_secundarias,
        'categorias': categorias,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'filtros_aplicados': {
            'categoria': categoria_id,
            'precio_min': precio_min,
            'precio_max': precio_max,
            'descuento': descuento,
            'disponible': disponible,
            'ordenar': ordenar,
            'buscar': buscar,
        }
    }
    
    # Si es una petición HTMX, solo devolver el grid de productos
    if request.headers.get('HX-Request'):
        return render(request, 'productos/partials/product_grid.html', context)
    
    return render(request, 'productos/lista_hentai_modern.html', context)

def filtros_ajax(request):
    """Vista AJAX para filtros de productos sin recargar página"""
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Obtener productos con filtros
        productos = Producto.objects.filter(activo=True)
        
        # Filtro por búsqueda
        q = request.GET.get('q', '').strip()
        if q:
            productos = productos.filter(
                Q(nombre__icontains=q) | Q(descripcion__icontains=q)
            )
        
        # Filtro por categoría
        categoria_id = request.GET.get('categoria')
        if categoria_id and categoria_id.isdigit():
            productos = productos.filter(categoria_id=categoria_id)
        
        # Filtro por precio máximo
        precio_max = request.GET.get('precio_max')
        if precio_max and precio_max.replace('.', '').isdigit():
            productos = productos.filter(precio_final__lte=float(precio_max))
        
        # Aplicar ordenamiento
        orden = request.GET.get('orden', 'nombre')
        if orden == 'precio_asc':
            productos = productos.order_by('precio')
        elif orden == 'precio_desc':
            productos = productos.order_by('-precio')
        elif orden == 'nombre':
            productos = productos.order_by('nombre')
        elif orden == 'fecha':
            productos = productos.order_by('-fecha_creacion')
        
        # Paginación
        productos = productos.select_related('categoria')[:50]  # Limitar a 50 productos
        
        context = {
            'productos': productos,
            'productos_count': productos.count(),
        }
        
        return render(request, 'productos/partials/product_grid.html', context)
    
    return JsonResponse({'error': 'No es una petición AJAX'}, status=400)
    
    return JsonResponse({'error': 'Petición no válida'}, status=400)

def detalle_producto(request, producto_id):
    """Detalle de producto con información completa"""
    producto = get_object_or_404(Producto, id=producto_id, activo=True)
    
    # Verificar si está en favoritos del usuario
    es_favorito = False
    if request.user.is_authenticated:
        es_favorito = Favorito.objects.filter(usuario=request.user, producto=producto).exists()
    
    # Obtener productos relacionados de la misma categoría
    productos_relacionados = []
    if producto.categoria:
        productos_relacionados = Producto.objects.filter(
            categoria=producto.categoria,
            activo=True,
            stock__gt=0
        ).exclude(id=producto.id).select_related('categoria')[:8]
    
    # Obtener tallas y colores disponibles
    tallas = []
    if producto.tiene_tallas and producto.tallas_disponibles:
        tallas = [t.strip() for t in producto.tallas_disponibles.split(',') if t.strip()]
    
    colores = producto.get_colores_lista()
    
    # Galería de imágenes
    imagenes_galeria = producto.imagenes_galeria
    
    context = {
        'producto': producto,
        'es_favorito': es_favorito,
        'productos_relacionados': productos_relacionados,
        'tallas_disponibles': tallas,
        'colores_disponibles': colores,
        'imagenes_galeria': imagenes_galeria,
        'tiene_galeria': len(imagenes_galeria) > 1,
    }
    return render(request, 'productos/detalle.html', context)

def productos_por_categoria(request, categoria_slug):
    """Vista específica para mostrar productos de una categoría"""
    categoria = get_object_or_404(Categoria, slug=categoria_slug, activa=True)
    
    # Obtener productos de la categoría
    productos = Producto.objects.filter(
        categoria=categoria,
        activo=True
    ).select_related('categoria')
    
    # Aplicar filtros adicionales
    precio_min = request.GET.get('precio_min')
    precio_max = request.GET.get('precio_max')
    descuento = request.GET.get('descuento')
    disponible = request.GET.get('disponible')
    ordenar = request.GET.get('ordenar', '')
    buscar = request.GET.get('q', '')
    
    # Filtros de precio
    if precio_min:
        productos = productos.filter(precio__gte=precio_min)
    if precio_max:
        productos = productos.filter(precio__lte=precio_max)
    
    # Filtro de descuentos
    if descuento == 'si':
        productos = productos.filter(precio_oferta__isnull=False)
    
    # Filtro de disponibilidad
    if disponible == 'si':
        productos = productos.filter(stock__gt=0)
    
    # Búsqueda
    if buscar:
        productos = productos.filter(
            Q(nombre__icontains=buscar) |
            Q(descripcion__icontains=buscar)
        )
    
    # Ordenamiento
    if ordenar == 'precio_asc':
        productos = productos.order_by('precio')
    elif ordenar == 'precio_desc':
        productos = productos.order_by('-precio')
    elif ordenar == 'nombre_asc':
        productos = productos.order_by('nombre')
    elif ordenar == 'nombre_desc':
        productos = productos.order_by('-nombre')
    elif ordenar == 'fecha_asc':
        productos = productos.order_by('fecha_creacion')
    elif ordenar == 'fecha_desc':
        productos = productos.order_by('-fecha_creacion')
    else:
        productos = productos.order_by('-destacado', '-fecha_creacion')
    
    # Paginación
    paginator = Paginator(productos, 12)  # 12 productos por página
    page = request.GET.get('page', 1)
    productos_paginados = paginator.get_page(page)
    
    # Obtener todas las categorías para el menú
    todas_categorias = Categoria.objects.filter(activa=True).order_by('nombre')
    
    context = {
        'categoria': categoria,
        'productos': productos_paginados,
        'categorias': todas_categorias,
        'total_productos': productos.count(),
        'filtros_aplicados': {
            'precio_min': precio_min,
            'precio_max': precio_max,
            'descuento': descuento,
            'disponible': disponible,
            'ordenar': ordenar,
            'buscar': buscar,
        }
    }
    
    return render(request, 'productos/categoria_productos.html', context)

@login_required
def perfil(request):
    """Vista del perfil del usuario moderno con todas las funcionalidades"""
    from django.utils import timezone
    from datetime import datetime
    
    # Manejar actualización de perfil
    if request.method == 'POST':
        try:
            # Actualizar datos básicos del usuario
            user = request.user
            user.username = request.POST.get('username', user.username)
            user.email = request.POST.get('email', user.email)
            user.first_name = request.POST.get('first_name', '')
            user.last_name = request.POST.get('last_name', '')
            user.save()
            
            # Crear o actualizar perfil extendido
            from authentication.models import UserProfile
            profile, created = UserProfile.objects.get_or_create(user=user)
            
            # Manejar avatar si se subió
            if request.FILES.get('avatar'):
                profile.avatar = request.FILES['avatar']
                profile.save()
            
            messages.success(request, '¡Perfil actualizado exitosamente! 🎉')
            return redirect('perfil')
            
        except Exception as e:
            messages.error(request, f'Error al actualizar perfil: {str(e)}')
    
    # Obtener datos para mostrar
    # Favoritos del usuario
    favoritos = Favorito.objects.filter(usuario=request.user).select_related('producto')
    
    # Órdenes del usuario
    ordenes = Orden.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    
    # Direcciones del usuario (mock por ahora)
    direcciones = []  # TODO: Implementar modelo de direcciones
    
    # Calcular estadísticas
    total_productos = Producto.objects.filter(activo=True).count()
    dias_miembro = (timezone.now().date() - request.user.date_joined.date()).days
    
    # Items en carrito
    carrito = request.session.get('carrito', {})
    items_carrito = sum(carrito.values()) if carrito else 0
    
    context = {
        'user': request.user,
        'favoritos': favoritos,
        'ordenes': ordenes,
        'direcciones': direcciones,
        'total_productos': total_productos,
        'dias_miembro': dias_miembro,
        'items_carrito': items_carrito,
    }
    
    # Agregar estadísticas adicionales para admin
    if request.user.is_staff:
        from django.contrib.auth.models import User
        from authentication.models import Factura
        
        context.update({
            'total_usuarios': User.objects.count(),
            'total_ordenes': Orden.objects.count(),
            'total_facturas': Factura.objects.count(),
        })
    
    return render(request, 'authentication/perfil_modern.html', context)

def terminos(request):
    """Términos y condiciones"""
    return render(request, 'productos/terminos.html')

# ✅ VIEWS DE REDIRECCIÓN PARA LOGIN
def login_view(request):
    """Redirigir a login de la app login"""
    return redirect('/admin/')

def register(request):
    """Redirigir a register de la app login"""
    return redirect('/admin/')

def logout_view(request):
    """Logout básico - funciona con GET y POST"""
    logout(request)
    messages.success(request, '¡Hasta luego! Has cerrado sesión exitosamente.')
    return redirect('lista_productos')

def redirect_to_auth_login(request):
    """Redireccionar al login de authentication"""
    return redirect('authentication:web_login')

def redirect_to_auth_register(request):
    """Redireccionar al registro de authentication"""
    return redirect('authentication:web_register')

# ✅ CARRITO USANDO SESIONES (NO MODELOS)
@login_required
def ver_carrito(request):
    """Ver carrito usando sesiones"""
    carrito = request.session.get('carrito', {})
    productos_carrito = []
    total = 0
    
    for producto_id, cantidad in carrito.items():
        try:
            producto = Producto.objects.get(id=producto_id, activo=True)
            subtotal = producto.precio * cantidad
            productos_carrito.append({
                'producto': producto,
                'cantidad': cantidad,
                'subtotal': subtotal
            })
            total += subtotal
        except Producto.DoesNotExist:
            # Remover producto que ya no existe
            del request.session['carrito'][producto_id]
            request.session.modified = True
    
    context = {
        'items': productos_carrito,  # ✅ USAR 'items' para compatibilidad
        'total': total,
        'cantidad_items': len(productos_carrito)
    }
    
    return render(request, 'productos/carrito_modern.html', context)

@login_required
def agregar_carrito(request, producto_id):
    """Agregar al carrito usando sesiones"""
    if request.method == 'POST':
        producto = get_object_or_404(Producto, id=producto_id, activo=True)
        cantidad = int(request.POST.get('cantidad', 1))
        
        # Verificar stock
        if cantidad > producto.stock:
            messages.error(request, f'Solo hay {producto.stock} unidades disponibles')
            return redirect('detalle_producto', producto_id=producto_id)
        
        # Obtener carrito de la sesión
        carrito = request.session.get('carrito', {})
        
        # Agregar o actualizar producto en carrito
        if str(producto_id) in carrito:
            nueva_cantidad = carrito[str(producto_id)] + cantidad
            if nueva_cantidad > producto.stock:
                messages.error(request, f'Solo hay {producto.stock} unidades disponibles')
                return redirect('detalle_producto', producto_id=producto_id)
            carrito[str(producto_id)] = nueva_cantidad
        else:
            carrito[str(producto_id)] = cantidad
        
        # Guardar carrito en sesión
        request.session['carrito'] = carrito
        request.session.modified = True
        
        messages.success(request, f'{producto.nombre} agregado al carrito')
        return redirect('ver_carrito')
    
    return redirect('lista_productos')

@login_required
def proceso_pago(request):
    """Proceso de pago usando sesiones"""
    carrito = request.session.get('carrito', {})
    
    if not carrito:
        messages.warning(request, 'Tu carrito está vacío.')
        return redirect('lista_productos')
    
    items = []
    total = 0
    
    # Convertir carrito de sesión a items
    for producto_id, cantidad in carrito.items():
        try:
            producto = Producto.objects.get(id=producto_id, activo=True)
            subtotal = producto.precio * cantidad
            items.append({
                'producto': producto,
                'cantidad': cantidad,
                'subtotal': subtotal
            })
            total += subtotal
        except Producto.DoesNotExist:
            # Remover producto que ya no existe
            del request.session['carrito'][producto_id]
            request.session.modified = True
    
    if request.method == 'POST':
        # Procesar pago
        metodo_pago = request.POST.get('metodo_pago', 'tarjeta')
        direccion = request.POST.get('direccion', '')
        
        # ✅ CREAR ORDEN
        orden = Orden.objects.create(
            usuario=request.user,
            total=total,
            estado='pendiente',
            metodo_pago=metodo_pago,
            direccion_envio=direccion
        )
        
        # Limpiar el carrito después de crear la orden
        request.session['carrito'] = {}
        request.session.modified = True
        
        messages.success(request, f'¡Orden #{orden.numero_orden} creada exitosamente!')
        return render(request, 'productos/pago_exitoso.html', {
            'total': total, 
            'orden': orden
        })
    
    return render(request, 'productos/proceso_pago_modern.html', {
        'items': items, 
        'total': total
    })

def generate_simple_response(message, user):
    """Respuestas inteligentes del chatbot con conocimiento completo del marketplace"""
    message_lower = message.lower().strip()
    
    # ===== SALUDOS =====
    if any(word in message_lower for word in ['hola', 'hey', 'buenas', 'hi', 'buenos dias', 'buenas tardes', 'buenas noches']):
        if user.is_authenticated:
            return f"¡Hola {user.username}! 👋✨\n\n¿En qué puedo ayudarte hoy?\n\n🛍️ Ver productos\n❤️ Mis favoritos\n🛒 Mi carrito\n📦 Mis pedidos\n💳 Procesar pago\n🎁 Promociones activas"
        else:
            return "¡Hola! 👋 Bienvenido a **LUST MarketPlace** 🔥\n\nPuedo ayudarte con:\n\n🛍️ Ver productos disponibles\n🔐 Información sobre registro\n📦 Envíos y entregas\n💳 Métodos de pago\n\n¿Qué necesitas saber?"
    
    # ===== PRODUCTOS =====
    if any(word in message_lower for word in ['producto', 'mostrar', 'disponible', 'catalogo', 'tienda']):
        productos = Producto.objects.filter(activo=True, stock__gt=0).order_by('-fecha_creacion')[:5]
        if productos:
            response = "🛍️ **Productos Destacados Disponibles:**\n\n"
            for i, p in enumerate(productos, 1):
                precio_display = f"${p.precio_oferta}" if p.precio_oferta else f"${p.precio}"
                badge = "🔥" if p.destacado else "⭐" if p.nuevo else "💎" if p.mas_vendido else "📦"
                response += f"{badge} **{p.nombre}**\n"
                response += f"💰 Precio: {precio_display}\n"
                response += f"📦 Stock: {p.stock} unidades\n"
                if p.categoria:
                    response += f"🏷️ Categoría: {p.categoria.nombre}\n"
                response += "\n"
            response += "💡 Visita la página principal para ver todos los productos y agregarlos al carrito."
            return response
        else:
            return "😔 Actualmente no tenemos productos en stock, pero pronto tendremos novedades increíbles. ¡Vuelve pronto!"
    
    # ===== CATEGORÍAS =====
    if any(word in message_lower for word in ['categoria', 'categorias', 'tipo', 'tipos']):
        from .models import Categoria
        categorias = Categoria.objects.filter(activa=True).annotate(
            total_productos=Count('producto', filter=Q(producto__activo=True))
        )
        if categorias:
            response = "🏷️ **Categorías Disponibles:**\n\n"
            for cat in categorias:
                response += f"📂 **{cat.nombre}** ({cat.total_productos} productos)\n"
            response += "\n¿Te interesa alguna categoría en particular?"
            return response
        return "Aún no tenemos categorías configuradas."
    
    # ===== PROMOCIONES =====
    if any(word in message_lower for word in ['promocion', 'promociones', 'oferta', 'ofertas', 'descuento', 'rebaja']):
        promociones = Promocion.objects.filter(activa=True, esta_activa=True)[:3]
        if promociones:
            response = "🎁 **Promociones Activas:**\n\n"
            for i, promo in enumerate(promociones, 1):
                response += f"✨ **{promo.titulo}**\n"
                if promo.subtitulo:
                    response += f"📝 {promo.subtitulo}\n"
                if promo.descuento_porcentaje:
                    response += f"💰 {promo.descuento_porcentaje}% de descuento\n"
                response += "\n"
            response += "🔥 ¡Aprovecha estas ofertas mientras duren!"
            return response
        return "😔 No hay promociones activas en este momento, pero pronto tendremos ofertas increíbles."
    
    # ===== CARRITO =====
    if any(word in message_lower for word in ['carrito', 'carro', 'compra', 'agregar']):
        if user.is_authenticated:
            from Carrito.models import Carrito, ItemCarrito
            carrito, _ = Carrito.objects.get_or_create(usuario=user)
            items = ItemCarrito.objects.filter(carrito=carrito)
            
            if items.exists():
                response = "🛒 **Tu Carrito:**\n\n"
                total = 0
                for item in items:
                    subtotal = item.producto.precio_final * item.cantidad
                    total += subtotal
                    response += f"📦 {item.producto.nombre}\n"
                    response += f"   Cantidad: {item.cantidad} × ${item.producto.precio_final} = ${subtotal}\n\n"
                response += f"💰 **Total: ${total}**\n\n"
                response += "¿Listo para proceder al pago?"
                return response
            else:
                return "🛒 Tu carrito está vacío.\n\n💡 Explora nuestros productos y agrega los que te gusten."
        else:
            return "🔐 Para usar el carrito necesitas **iniciar sesión** primero.\n\n📝 ¿Necesitas ayuda para registrarte?"
    
    # ===== FAVORITOS =====
    if any(word in message_lower for word in ['favorito', 'favoritos', 'me gusta', 'guardados']):
        if user.is_authenticated:
            from .models import Favorito
            favoritos = Favorito.objects.filter(usuario=user).select_related('producto')
            
            if favoritos.exists():
                response = "❤️ **Tus Productos Favoritos:**\n\n"
                for fav in favoritos[:5]:
                    response += f"💖 {fav.producto.nombre}\n"
                    response += f"   💰 ${fav.producto.precio_final}\n\n"
                response += f"Total: {favoritos.count()} productos favoritos"
                return response
            else:
                return "❤️ Aún no tienes productos favoritos.\n\n💡 Haz clic en el corazón ❤️ en cualquier producto para agregarlo a favoritos."
        else:
            return "🔐 Para ver tus favoritos necesitas **iniciar sesión**."
    
    # ===== PEDIDOS/ÓRDENES =====
    if any(word in message_lower for word in ['pedido', 'pedidos', 'orden', 'ordenes', 'compra anterior', 'historial']):
        if user.is_authenticated:
            ordenes = Orden.objects.filter(usuario=user).order_by('-fecha_creacion')[:3]
            
            if ordenes.exists():
                response = "📦 **Tus Últimos Pedidos:**\n\n"
                for orden in ordenes:
                    estado_emoji = {
                        'pendiente': '⏳',
                        'procesando': '🔄',
                        'enviado': '📮',
                        'entregado': '✅',
                        'cancelado': '❌'
                    }.get(orden.estado, '📦')
                    
                    response += f"{estado_emoji} **Orden #{orden.numero_orden}**\n"
                    response += f"   Estado: {orden.get_estado_display()}\n"
                    response += f"   Total: ${orden.total}\n"
                    response += f"   Fecha: {orden.fecha_creacion.strftime('%d/%m/%Y')}\n\n"
                return response
            else:
                return "� Aún no tienes pedidos.\n\n🛍️ ¡Explora nuestros productos y haz tu primera compra!"
        else:
            return "🔐 Para ver tus pedidos necesitas **iniciar sesión**."
    
    # ===== MÉTODOS DE PAGO =====
    if any(word in message_lower for word in ['pago', 'pagar', 'metodo de pago', 'tarjeta', 'efectivo']):
        return "💳 **Métodos de Pago Disponibles:**\n\n✅ Tarjeta de Crédito/Débito\n✅ Transferencia Bancaria\n✅ Pago contra entrega (efectivo)\n✅ PayPal\n\n🔒 Todos los pagos son seguros y encriptados.\n\n¿Tienes alguna duda sobre el proceso de pago?"
    
    # ===== ENVÍOS =====
    if any(word in message_lower for word in ['envio', 'envios', 'entrega', 'delivery', 'shipping']):
        return "📦 **Información de Envíos:**\n\n🚚 Envío estándar (3-5 días)\n⚡ Envío express (1-2 días)\n🏠 Recogida en tienda\n\n💰 Envío GRATIS en compras mayores a $50\n\n📍 ¿Necesitas agregar una dirección de envío?"
    
    # ===== REGISTRO/LOGIN =====
    if any(word in message_lower for word in ['registro', 'registrar', 'crear cuenta', 'cuenta nueva']):
        return "📝 **Crear Cuenta Nueva:**\n\n1️⃣ Haz clic en 'Registrarse' en la parte superior\n2️⃣ Completa tus datos personales\n3️⃣ Verifica tu email\n4️⃣ ¡Listo! Ya puedes comprar\n\n🎁 Regístrate y obtén descuentos exclusivos en tu primera compra."
    
    if any(word in message_lower for word in ['login', 'iniciar sesion', 'entrar', 'ingresar']):
        if user.is_authenticated:
            return f"✅ Ya has iniciado sesión como **{user.username}**\n\n¿Qué necesitas hacer?"
        else:
            return "🔐 **Iniciar Sesión:**\n\nHaz clic en el botón 'Iniciar Sesión' en la parte superior de la página.\n\n¿Olvidaste tu contraseña? Podemos ayudarte a recuperarla."
    
    # ===== PERFIL =====
    if any(word in message_lower for word in ['perfil', 'mi cuenta', 'datos', 'informacion personal']):
        if user.is_authenticated:
            return f"� **Tu Perfil - {user.username}**\n\n📧 Email: {user.email}\n\nPuedes actualizar tu información desde:\n'Mi Perfil' → 'Editar Perfil'\n\n¿Necesitas cambiar algo específico?"
        else:
            return "🔐 Para ver tu perfil necesitas **iniciar sesión** primero."
    
    # ===== RESEÑAS =====
    if any(word in message_lower for word in ['resena', 'reseña', 'opinion', 'comentario', 'calificacion']):
        return "⭐ **Reseñas y Calificaciones:**\n\nPuedes dejar tu opinión en cualquier producto que hayas comprado.\n\n📝 Tu opinión nos ayuda a mejorar y ayuda a otros compradores.\n\n¿Quieres dejar una reseña en algún producto?"
    
    # ===== AYUDA/CONTACTO =====
    if any(word in message_lower for word in ['ayuda', 'soporte', 'contacto', 'problema', 'error']):
        return "🆘 **Centro de Ayuda:**\n\n📧 Email: soporte@lustmarketplace.com\n📱 WhatsApp: +1 234-567-8900\n⏰ Horario: Lun-Vie 9AM-6PM\n\n¿En qué puedo ayudarte específicamente?"
    
    # ===== DESPEDIDAS =====
    if any(word in message_lower for word in ['gracias', 'bye', 'adios', 'chao', 'hasta luego']):
        return "¡De nada! 😊✨\n\nSi necesitas algo más, estaré aquí para ayudarte.\n\n¡Que tengas un excelente día! 🌟"
    
    # ===== BÚSQUEDA ESPECÍFICA DE PRODUCTOS =====
    if any(word in message_lower for word in ['buscar', 'busco', 'quiero', 'necesito']):
        # Intentar extraer nombre del producto
        palabras_clave = message_lower.replace('buscar', '').replace('busco', '').replace('quiero', '').replace('necesito', '').strip()
        if palabras_clave:
            productos = Producto.objects.filter(
                Q(nombre__icontains=palabras_clave) | Q(descripcion__icontains=palabras_clave),
                activo=True,
                stock__gt=0
            )[:3]
            
            if productos.exists():
                response = f"🔍 Encontré estos productos relacionados con '{palabras_clave}':\n\n"
                for p in productos:
                    response += f"✨ **{p.nombre}**\n"
                    response += f"   💰 ${p.precio_final}\n"
                    response += f"   📦 Stock: {p.stock}\n\n"
                return response
            else:
                return f"😔 No encontré productos con '{palabras_clave}'.\n\n💡 ¿Quieres ver todos nuestros productos disponibles?"
    
    # ===== RESPUESTA POR DEFECTO =====
    return """🤖 **Asistente Virtual de LUST MarketPlace**

¡Estoy aquí para ayudarte! Puedo asistirte con:

🛍️ **Productos** - Ver catálogo y disponibilidad
🎁 **Promociones** - Ofertas y descuentos activos
🛒 **Carrito** - Gestión de tu carrito de compras
❤️ **Favoritos** - Productos guardados
📦 **Pedidos** - Estado de tus órdenes
💳 **Pagos** - Métodos y proceso de pago
🚚 **Envíos** - Información de entrega
👤 **Perfil** - Tu cuenta y configuración
🆘 **Ayuda** - Soporte y contacto

¿Qué necesitas saber?"""

# ✅ VISTAS PARA FAVORITOS
@login_required
@login_required
def agregar_favorito(request, producto_id):
    """Agregar producto a favoritos"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)
    
    try:
        producto = get_object_or_404(Producto, id=producto_id, activo=True)
        favorito, created = Favorito.objects.get_or_create(
            usuario=request.user,
            producto=producto
        )
        
        if created:
            return JsonResponse({
                'success': True, 
                'message': f'❤️ {producto.nombre} agregado a favoritos',
                'es_favorito': True
            })
        else:
            return JsonResponse({
                'success': True, 
                'message': 'Ya está en tus favoritos',
                'es_favorito': True
            })
            
    except Producto.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Producto no encontrado'}, status=404)
    except Exception as e:
        print(f"❌ Error en agregar_favorito: {str(e)}")  # Debug
        return JsonResponse({'success': False, 'message': f'Error al agregar a favoritos: {str(e)}'}, status=500)

@login_required
def quitar_favorito(request, producto_id):
    """Quitar producto de favoritos"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)
    
    try:
        favorito = get_object_or_404(Favorito, usuario=request.user, producto_id=producto_id)
        producto_nombre = favorito.producto.nombre
        favorito.delete()
        return JsonResponse({
            'success': True, 
            'message': f'💔 {producto_nombre} quitado de favoritos',
            'es_favorito': False
        })
    except Favorito.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'El producto no está en favoritos'}, status=404)
    except Exception as e:
        print(f"❌ Error en quitar_favorito: {str(e)}")  # Debug
        return JsonResponse({'success': False, 'message': f'Error al quitar de favoritos: {str(e)}'}, status=500)

@login_required
def toggle_favorito(request, favorito_id):
    """Alternar favorito (quitar si existe, agregar si no existe) usando el ID del favorito"""
    if request.method == 'POST':
        try:
            from .models import Favorito
            # Intentar encontrar y eliminar el favorito por su ID
            favorito = get_object_or_404(Favorito, id=favorito_id, usuario=request.user)
            favorito.delete()
            return JsonResponse({
                'success': True, 
                'action': 'removed',
                'message': '💔 Producto quitado de favoritos'
            })
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'message': f'Error al procesar favorito: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

@login_required
def lista_favoritos(request):
    """Lista de productos favoritos del usuario"""
    from .models import Favorito
    favoritos = Favorito.objects.filter(usuario=request.user).select_related('producto')
    return render(request, 'productos/favoritos.html', {'favoritos': favoritos})

# ===== VISTAS DE ADMINISTRADOR =====
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def admin_productos(request):
    """Vista para administrar productos desde la web"""
    productos = Producto.objects.all().order_by('-id')
    
    context = {
        'productos': productos,
        'total_productos': productos.count(),
        'productos_activos': productos.filter(activo=True).count(),
        'productos_inactivos': productos.filter(activo=False).count(),
    }
    
    return render(request, 'productos/admin/admin_productos.html', context)

@staff_member_required
def admin_usuarios(request):
    """Vista para administrar usuarios"""
    usuarios = User.objects.all().order_by('-date_joined')
    
    context = {
        'usuarios': usuarios,
        'total_usuarios': usuarios.count(),
        'usuarios_staff': usuarios.filter(is_staff=True).count(),
        'usuarios_activos': usuarios.filter(is_active=True).count(),
    }
    
    return render(request, 'productos/admin/admin_usuarios.html', context)

@staff_member_required
def editar_producto(request, producto_id):
    """Editar producto desde la web"""
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == 'POST':
        # Actualizar campos del producto
        producto.nombre = request.POST.get('nombre', producto.nombre)
        producto.descripcion = request.POST.get('descripcion', producto.descripcion)
        producto.precio = float(request.POST.get('precio', producto.precio))
        producto.stock = int(request.POST.get('stock', producto.stock))
        producto.activo = request.POST.get('activo') == 'on'
        
        # Manejar nueva imagen si se proporciona
        if 'imagen' in request.FILES:
            producto.imagen = request.FILES['imagen']
        
        producto.save()
        messages.success(request, f'Producto "{producto.nombre}" actualizado exitosamente.')
        return redirect('admin_productos')
    
    context = {'producto': producto}
    return render(request, 'productos/admin/editar_producto.html', context)

@staff_member_required
def eliminar_producto(request, producto_id):
    """Eliminar producto (marcar como inactivo)"""
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == 'POST':
        producto.activo = False
        producto.save()
        messages.success(request, f'Producto "{producto.nombre}" desactivado exitosamente.')
    
    return redirect('admin_productos')

@staff_member_required
def crear_producto(request):
    """Crear nuevo producto desde la web"""
    if request.method == 'POST':
        try:
            producto = Producto.objects.create(
                nombre=request.POST.get('nombre'),
                descripcion=request.POST.get('descripcion'),
                precio=float(request.POST.get('precio')),
                stock=int(request.POST.get('stock')),
                activo=request.POST.get('activo') == 'on'
            )
            
            # Manejar imagen si se proporciona
            if 'imagen' in request.FILES:
                producto.imagen = request.FILES['imagen']
                producto.save()
            
            messages.success(request, f'Producto "{producto.nombre}" creado exitosamente.')
            return redirect('admin_productos')
            
        except Exception as e:
            messages.error(request, f'Error al crear el producto: {str(e)}')
    
    return render(request, 'productos/admin/crear_producto.html')

@staff_member_required
def toggle_usuario_staff(request, usuario_id):
    """Cambiar estado de staff de un usuario"""
    if request.method == 'POST':
        usuario = get_object_or_404(User, id=usuario_id)
        usuario.is_staff = not usuario.is_staff
        usuario.save()
        
        estado = "administrador" if usuario.is_staff else "usuario regular"
        messages.success(request, f'Usuario "{usuario.username}" ahora es {estado}.')
    
    return redirect('admin_usuarios')

@staff_member_required
def toggle_usuario_activo(request, usuario_id):
    """Activar/desactivar usuario"""
    if request.method == 'POST':
        usuario = get_object_or_404(User, id=usuario_id)
        usuario.is_active = not usuario.is_active
        usuario.save()
        
        estado = "activado" if usuario.is_active else "desactivado"
        messages.success(request, f'Usuario "{usuario.username}" {estado} exitosamente.')
    
    return redirect('admin_usuarios')


@csrf_exempt
def promocion_click(request):
    """Registrar click en promoción para analytics"""
    if request.method == 'POST':
        promocion_id = request.POST.get('promocion_id')
        if promocion_id:
            try:
                promocion = Promocion.objects.get(id=promocion_id)
                promocion.incrementar_click()
                
                # Registrar vista detallada si el usuario está autenticado
                if request.user.is_authenticated:
                    PromocionView.objects.create(
                        promocion=promocion,
                        usuario=request.user,
                        ip_address=request.META.get('REMOTE_ADDR', ''),
                        user_agent=request.META.get('HTTP_USER_AGENT', '')
                    )
                
                return JsonResponse({'status': 'success'})
            except Promocion.DoesNotExist:
                pass
    
    return JsonResponse({'status': 'error'})

def detalle_promocion(request, promocion_id):
    """Vista detallada de una promoción"""
    promocion = get_object_or_404(Promocion, id=promocion_id, activa=True)
    
    # Incrementar contador de vistas
    promocion.incrementar_vista()
    
    # Obtener productos relacionados
    productos = promocion.productos.filter(activo=True)
    
    # Si no hay productos específicos, mostrar productos de la categoría
    if not productos.exists() and promocion.categoria:
        productos = Producto.objects.filter(
            categoria=promocion.categoria,
            activo=True
        )[:12]
    
    context = {
        'promocion': promocion,
        'productos': productos,
    }
    
    return render(request, 'productos/detalle_promocion.html', context)

def detalle_modal(request, producto_id):
    """Vista modal para mostrar detalles rápidos del producto"""
    producto = get_object_or_404(Producto, id=producto_id, activo=True)
    
    # Verificar si está en favoritos
    es_favorito = False
    if request.user.is_authenticated:
        es_favorito = Favorito.objects.filter(usuario=request.user, producto=producto).exists()
    
    context = {
        'producto': producto,
        'es_favorito': es_favorito,
    }
    
    return render(request, 'productos/partials/producto_modal.html', context)

@login_required
@csrf_exempt
@login_required
def toggle_favorito_producto(request, producto_id):
    """Toggle de favoritos con HTMX - Mejorado con validaciones"""
    if request.method != 'POST':
        return JsonResponse({
            'status': 'error',
            'mensaje': 'Método no permitido'
        }, status=405)
    
    try:
        producto = get_object_or_404(Producto, id=producto_id, activo=True)
        
        # Intentar obtener o crear el favorito
        favorito, creado = Favorito.objects.get_or_create(
            usuario=request.user,
            producto=producto
        )
        
        if not creado:
            # Si ya existía, lo eliminamos
            favorito.delete()
            es_favorito = False
            mensaje = f'💔 {producto.nombre} eliminado de favoritos'
        else:
            # Si es nuevo, está agregado
            es_favorito = True
            mensaje = f'💖 {producto.nombre} agregado a favoritos'
        
        # Respuesta JSON para AJAX
        return JsonResponse({
            'status': 'success',
            'es_favorito': es_favorito,
            'mensaje': mensaje
        })
        
    except Producto.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'mensaje': 'Producto no encontrado'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'mensaje': f'Error al procesar favorito: {str(e)}'
        }, status=500)


def lista_promociones_api(request):
    """API para obtener promociones activas (para HTMX)"""
    tipo = request.GET.get('tipo', 'todas')
    
    promociones = Promocion.objects.filter(
        activa=True,
        fecha_inicio__lte=timezone.now(),
        fecha_fin__gte=timezone.now()
    )
    
    if tipo == 'hero':
        promociones = promociones.filter(posicion='hero')
    elif tipo == 'secundarias':
        promociones = promociones.filter(posicion='secundaria')
    
    promociones = promociones.order_by('orden')[:10]
    
    data = []
    for promo in promociones:
        data.append({
            'id': promo.id,
            'titulo': promo.titulo,
            'subtitulo': promo.subtitulo,
            'descripcion': promo.descripcion,
            'tipo': promo.get_tipo_display(),
            'imagen': promo.imagen_principal.url if promo.imagen_principal else '',
            'url': promo.get_url_destino(),
            'descuento': float(promo.descuento_porcentaje) if promo.descuento_porcentaje else 0,
            'dias_restantes': promo.dias_restantes,
            'color_primary': promo.color_primary,
            'color_secondary': promo.color_secondary,
            'boton_texto': promo.boton_texto,
        })
    
    return JsonResponse({'promociones': data})


def detalle_promocion(request, promocion_id):
    """Vista detallada de una promoción con productos relacionados"""
    promocion = get_object_or_404(Promocion, id=promocion_id, activa=True)
    
    # Incrementar contador de vistas
    promocion.incrementar_vista()
    
    # Obtener productos de la promoción
    productos = promocion.productos.filter(activo=True)
    
    # Si no hay productos específicos, mostrar productos de la categoría
    if not productos.exists() and promocion.categoria:
        productos = Producto.objects.filter(
            categoria=promocion.categoria,
            activo=True
        )[:12]
    
    # ===== PRODUCTOS RELACIONADOS DE LA MISMA CATEGORÍA =====
    productos_relacionados = []
    
    # Obtener categorías de los productos en la promoción
    categorias_promocion = set()
    for producto in productos:
        if producto.categoria:
            categorias_promocion.add(producto.categoria.id)
    
    # Si la promoción tiene categoría directa, agregarla
    if promocion.categoria:
        categorias_promocion.add(promocion.categoria.id)
    
    # Calcular rango de precios de los productos en promoción
    precios = [p.precio_oferta if p.precio_oferta else p.precio for p in productos if p.precio]
    precio_min = min(precios) * 0.7 if precios else 0  # 30% menos
    precio_max = max(precios) * 1.3 if precios else 999999  # 30% más
    
    # Obtener productos relacionados de las mismas categorías
    if categorias_promocion:
        # Excluir productos que ya están en la promoción
        productos_ids_promocion = list(productos.values_list('id', flat=True))
        
        productos_relacionados = Producto.objects.filter(
            categoria_id__in=categorias_promocion,
            activo=True,
            stock__gt=0,  # Solo productos con stock
            precio__gte=precio_min,  # Rango de precio similar
            precio__lte=precio_max
        ).exclude(
            id__in=productos_ids_promocion  # Excluir los que ya están en la promoción
        ).select_related('categoria').order_by('-mas_vendido', '-vendidos', '-fecha_creacion')[:12]
    
    context = {
        'promocion': promocion,
        'productos': productos,
        'productos_relacionados': productos_relacionados,
        'tiene_relacionados': len(productos_relacionados) > 0,
    }
    
    return render(request, 'productos/detalle_promocion.html', context)


def detalle_modal(request, producto_id):
    """Vista modal para mostrar detalles rápidos del producto"""
    producto = get_object_or_404(Producto, id=producto_id, activo=True)
    
    # Verificar si está en favoritos
    es_favorito = False
    if request.user.is_authenticated:
        es_favorito = Favorito.objects.filter(usuario=request.user, producto=producto).exists()
    
    context = {
        'producto': producto,
        'es_favorito': es_favorito,
    }
    
    return render(request, 'productos/partials/producto_modal.html', context)


@staff_member_required  
def admin_promociones(request):
    """Vista de administración de promociones"""
    promociones = Promocion.objects.all().order_by('-fecha_creacion')
    
    # Estadísticas
    total_promociones = promociones.count()
    activas = promociones.filter(activa=True).count()
    expiradas = promociones.filter(fecha_fin__lt=timezone.now()).count()
    
    context = {
        'promociones': promociones,
        'total_promociones': total_promociones,
        'promociones_activas': activas,
        'promociones_expiradas': expiradas,
    }
    
    return render(request, 'productos/admin_promociones.html', context)


# ✅ VISTA PARA PRODUCTOS DE UNA PROMOCIÓN ESPECÍFICA
def productos_promocion(request, promocion_id):
    """Vista para mostrar productos de una promoción específica"""
    promocion = get_object_or_404(Promocion, id=promocion_id, activa=True)
    
    # Incrementar contador de clicks
    promocion.click_conteo += 1
    promocion.save()
    
    # Obtener productos de la promoción
    productos = promocion.productos.filter(activo=True)
    
    # Si no hay productos específicos, mostrar productos de la categoría
    if not productos.exists() and promocion.categoria:
        productos = Producto.objects.filter(categoria=promocion.categoria, activo=True)
    
    # Si aún no hay productos, mostrar productos destacados
    if not productos.exists():
        productos = Producto.objects.filter(activo=True, destacado=True)
    
    # Si aún no hay productos destacados, mostrar todos los productos activos
    if not productos.exists():
        productos = Producto.objects.filter(activo=True)[:12]  # Limitar a 12 productos
    
    # Aplicar descuento de la promoción si existe
    productos_con_descuento = []
    for producto in productos:
        precio_original = producto.precio
        precio_final = precio_original
        
        # Aplicar descuento de la promoción
        if promocion.descuento_porcentaje > 0:
            descuento = (promocion.descuento_porcentaje / 100) * precio_original
            precio_final = precio_original - descuento
        elif promocion.precio_especial:
            precio_final = promocion.precio_especial
        
        productos_con_descuento.append({
            'producto': producto,
            'precio_original': precio_original,
            'precio_final': precio_final,
            'descuento_promocion': promocion.descuento_porcentaje,
            'ahorro': precio_original - precio_final
        })
    
    context = {
        'promocion': promocion,
        'productos': productos_con_descuento,
        'tiene_descuento': promocion.descuento_porcentaje > 0 or promocion.precio_especial,
    }
    
    return render(request, 'productos/productos_promocion.html', context)


# ✅ FUNCIONES AJAX PARA CARRITO MODERNO
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
@login_required
def actualizar_cantidad_carrito(request):
    """Actualizar cantidad de producto en carrito vía AJAX"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            producto_id = str(data.get('producto_id'))
            nueva_cantidad = int(data.get('cantidad'))
            
            if nueva_cantidad <= 0:
                return JsonResponse({'success': False, 'error': 'Cantidad inválida'})
            
            # Verificar que el producto existe
            producto = get_object_or_404(Producto, id=producto_id, activo=True)
            
            # Verificar stock
            if nueva_cantidad > producto.stock:
                return JsonResponse({
                    'success': False, 
                    'error': f'Stock insuficiente. Disponible: {producto.stock}'
                })
            
            # Actualizar carrito en sesión
            carrito = request.session.get('carrito', {})
            carrito[producto_id] = nueva_cantidad
            request.session['carrito'] = carrito
            request.session.modified = True
            
            # Calcular nuevo total
            total = 0
            for pid, cantidad in carrito.items():
                try:
                    p = Producto.objects.get(id=pid, activo=True)
                    total += p.precio * cantidad
                except Producto.DoesNotExist:
                    pass
            
            return JsonResponse({
                'success': True,
                'nueva_cantidad': nueva_cantidad,
                'subtotal': float(producto.precio * nueva_cantidad),
                'total': float(total)
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@csrf_exempt 
@login_required
def eliminar_del_carrito(request):
    """Eliminar producto del carrito vía AJAX"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            producto_id = str(data.get('producto_id'))
            
            # Eliminar del carrito en sesión
            carrito = request.session.get('carrito', {})
            if producto_id in carrito:
                del carrito[producto_id]
                request.session['carrito'] = carrito
                request.session.modified = True
            
            # Calcular nuevo total
            total = 0
            for pid, cantidad in carrito.items():
                try:
                    p = Producto.objects.get(id=pid, activo=True)
                    total += p.precio * cantidad
                except Producto.DoesNotExist:
                    pass
            
            return JsonResponse({
                'success': True,
                'total': float(total),
                'items_count': len(carrito)
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@csrf_exempt
@login_required  
def vaciar_carrito(request):
    """Vaciar todo el carrito vía AJAX"""
    if request.method == 'POST':
        try:
            # Limpiar carrito de sesión
            request.session['carrito'] = {}
            request.session.modified = True
            
            return JsonResponse({
                'success': True,
                'message': 'Carrito vaciado exitosamente'
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})
