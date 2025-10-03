from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse  
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt  
from .models import Producto, Orden, Favorito  # ✅ IMPORTAR MODELOS NECESARIOS
from django.contrib.auth.models import User
from django.contrib import messages
import json
import random

def lista_productos(request):
    """Lista de productos - ACCESO PÚBLICO"""
    productos = Producto.objects.filter(activo=True)
    context = {'productos': productos}
    return render(request, 'productos/lista.html', context)

def detalle_producto(request, producto_id):
    """Detalle de producto"""
    producto = get_object_or_404(Producto, id=producto_id, activo=True)
    
    # Verificar si está en favoritos del usuario
    es_favorito = False
    if request.user.is_authenticated:
        es_favorito = Favorito.objects.filter(usuario=request.user, producto=producto).exists()
    
    context = {
        'producto': producto,
        'es_favorito': es_favorito
    }
    return render(request, 'productos/detalle.html', context)

@login_required
def perfil(request):
    """Vista del perfil del usuario con estadísticas"""
    from django.utils import timezone
    from datetime import datetime
    
    # Calcular estadísticas
    total_productos = Producto.objects.filter(activo=True).count()
    
    # Calcular días como miembro
    dias_miembro = (timezone.now().date() - request.user.date_joined.date()).days
    
    # Items en carrito para usuarios normales
    items_carrito = 0
    if not request.user.is_staff:
        carrito = request.session.get('carrito', {})
        items_carrito = sum(carrito.values()) if carrito else 0
    
    # Estadísticas adicionales para admin
    total_usuarios = 0
    if request.user.is_staff:
        total_usuarios = User.objects.count()
    
    context = {
        'user': request.user,
        'total_productos': total_productos,
        'dias_miembro': dias_miembro,
        'items_carrito': items_carrito,
        'total_usuarios': total_usuarios,
    }
    
    return render(request, 'productos/perfil.html', context)

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
    
    return render(request, 'productos/carrito.html', context)

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
        
        # Guardar información de la orden en la sesión para el módulo de payments
        request.session['orden_id'] = orden.id
        request.session['orden_total'] = float(total)
        
        # Redireccionar al módulo de payments
        return redirect('payments:checkout')  # Esto va al módulo payments
        
        messages.success(request, f'¡Orden #{orden.numero_orden} creada exitosamente!')
        return render(request, 'productos/pago_exitoso.html', {
            'total': total, 
            'orden': orden
        })
    
    return render(request, 'productos/pago.html', {
        'items': items, 
        'total': total
    })

@csrf_exempt
def chatbot_api(request):
    """API del chatbot - SIMPLIFICADA"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
            
            if not user_message:
                return JsonResponse({
                    'success': False, 
                    'error': 'Mensaje vacío'
                })
            
            # Respuesta simple sin IA por ahora
            response = generate_simple_response(user_message, request.user)
            
            return JsonResponse({
                'success': True,
                'response': response
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False, 
                'error': 'JSON inválido'
            })
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'error': f'Error interno: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

def generate_simple_response(message, user):
    """Respuestas simples del chatbot"""
    message_lower = message.lower().strip()
    
    # Saludos
    if any(word in message_lower for word in ['hola', 'hey', 'buenas', 'hi']):
        if user.is_authenticated:
            return f"¡Hola {user.username}! 👋 ¿En qué puedo ayudarte hoy?"
        else:
            return "¡Hola! 👋 ¿En qué puedo ayudarte? Para comprar necesitas iniciar sesión."
    
    # Productos
    if any(word in message_lower for word in ['producto', 'mostrar', 'disponible']):
        productos = Producto.objects.filter(activo=True, stock__gt=0)[:3]
        if productos:
            response = "🛍️ **Productos destacados:**\n\n"
            for i, p in enumerate(productos, 1):
                response += f"**{i}.** {p.nombre}\n💰 ${p.precio}\n📦 Stock: {p.stock}\n\n"
            response += "¿Te interesa alguno? Puedes ver más en la página principal."
            return response
        else:
            return "😔 No tenemos productos disponibles ahora, pero pronto tendremos novedades."
    
    # Carrito
    if 'carrito' in message_lower:
        if user.is_authenticated:
            return "🛒 Para ver tu carrito, haz clic en el ícono del carrito en la parte superior de la página."
        else:
            return "🔐 Para usar el carrito necesitas iniciar sesión primero."
    
    # Despedidas
    if any(word in message_lower for word in ['gracias', 'bye', 'adios']):
        return "¡De nada! 😊 Si necesitas algo más, estaré aquí. ¡Que tengas un buen día!"
    
    # Respuesta por defecto
    return "🤖 Puedo ayudarte con información sobre productos, precios y tu carrito. ¿Qué necesitas saber?"

# ✅ VISTAS PARA FAVORITOS
@login_required
def agregar_favorito(request, producto_id):
    """Agregar producto a favoritos"""
    if request.method == 'POST':
        try:
            from .models import Favorito
            producto = get_object_or_404(Producto, id=producto_id, activo=True)
            favorito, created = Favorito.objects.get_or_create(
                usuario=request.user,
                producto=producto
            )
            
            if created:
                return JsonResponse({'success': True, 'message': '❤️ Producto agregado a favoritos'})
            else:
                return JsonResponse({'success': False, 'message': 'Ya está en tus favoritos'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'Error al agregar a favoritos'})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

@login_required
def quitar_favorito(request, producto_id):
    """Quitar producto de favoritos"""
    if request.method == 'POST':
        try:
            from .models import Favorito
            favorito = get_object_or_404(Favorito, usuario=request.user, producto_id=producto_id)
            favorito.delete()
            return JsonResponse({'success': True, 'message': '💔 Producto quitado de favoritos'})
        except:
            return JsonResponse({'success': False, 'message': 'Error al quitar de favoritos'})
    
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
    
    return render(request, 'productos/admin_productos.html', context)

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
    
    return render(request, 'productos/admin_usuarios.html', context)

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
    return render(request, 'productos/editar_producto.html', context)

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
    
    return render(request, 'productos/crear_producto.html')

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


