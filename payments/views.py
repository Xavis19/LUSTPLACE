from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from productos.models import Producto, Orden  # ✅ IMPORTAR Orden DESDE productos
from django.contrib import messages
import uuid
from datetime import datetime

@login_required
def pago(request):
    """Proceso de pago usando carrito de sesión"""
    # Obtener productos del carrito desde la sesión
    carrito = request.session.get('carrito', {})
    
    if not carrito:
        messages.warning(request, 'Tu carrito está vacío.')
        return redirect('lista_productos')
    
    items = []
    total = 0
    
    # Convertir carrito de sesión a items
    for producto_id, cantidad in carrito.items():
        try:
            producto = Producto.objects.get(id=producto_id)
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
        
        # ✅ CREAR ORDEN CON EL MODELO IMPORTADO
        orden = Orden.objects.create(
            usuario=request.user,
            total=total,
            estado='pendiente',
            metodo_pago=metodo_pago,
            direccion_envio=direccion
        )
        
        # Limpiar carrito
        request.session['carrito'] = {}
        request.session.modified = True
        
        messages.success(request, f'¡Orden #{orden.numero_orden} creada exitosamente!')
        return render(request, 'productos/pago_exitoso.html', {'total': total, 'orden': orden})
    
    return render(request, 'productos/pago.html', {'items': items, 'total': total})

@login_required
def agregar_carrito(request, producto_id):
    """Agregar producto al carrito (método alternativo)"""
    producto = get_object_or_404(Producto, id=producto_id)
    
    # Obtener carrito de la sesión
    carrito = request.session.get('carrito', {})
    
    # Agregar producto
    if str(producto_id) in carrito:
        carrito[str(producto_id)] += 1
    else:
        carrito[str(producto_id)] = 1
    
    # Guardar carrito
    request.session['carrito'] = carrito
    request.session.modified = True
    
    messages.success(request, f'{producto.nombre} agregado al carrito')
    return redirect('lista_productos')

@login_required
def checkout(request):
    """Vista principal de checkout desde la orden creada"""
    orden_id = request.session.get('orden_id')
    
    if not orden_id:
        messages.error(request, 'No hay orden pendiente.')
        return redirect('lista_productos')
    
    try:
        orden = Orden.objects.get(id=orden_id, usuario=request.user)
        context = {
            'orden': orden,
            'total': orden.total
        }
        return render(request, 'payments/checkout.html', context)
    except Orden.DoesNotExist:
        messages.error(request, 'Orden no encontrada.')
        return redirect('lista_productos')

@login_required
def payment_success(request):
    """Vista de pago exitoso"""
    orden_id = request.session.get('orden_id')
    
    if orden_id:
        try:
            orden = Orden.objects.get(id=orden_id, usuario=request.user)
            orden.estado = 'completado'
            orden.save()
            
            # Limpiar sesión
            del request.session['orden_id']
            if 'orden_total' in request.session:
                del request.session['orden_total']
            request.session['carrito'] = {}
            request.session.modified = True
            
            messages.success(request, '¡Pago procesado exitosamente! Recibirás un email de confirmación.')
            
            context = {'orden': orden}
            return render(request, 'payments/success.html', context)
        except Orden.DoesNotExist:
            pass
    
    return redirect('lista_productos')

@login_required  
def payment_cancel(request):
    """Vista de pago cancelado"""
    messages.warning(request, 'Pago cancelado. Tu carrito sigue disponible.')
    return redirect('lista_productos')
