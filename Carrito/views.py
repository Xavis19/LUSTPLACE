from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from productos.models import Producto  # ✅ IMPORTAR DESDE productos, NO desde Carrito
from django.contrib import messages
from django.http import JsonResponse
import json

@login_required
def ver_carrito(request):
    """Vista para mostrar el carrito de compras"""
    # Obtener productos del carrito desde la sesión
    carrito = request.session.get('carrito', {})
    productos_carrito = []
    total = 0
    
    # Crear una lista de productos a eliminar para evitar modificar el diccionario durante la iteración
    productos_a_eliminar = []
    
    for producto_id, cantidad in carrito.items():
        try:
            producto = Producto.objects.get(id=producto_id)
            subtotal = producto.precio * cantidad
            productos_carrito.append({
                'id': producto_id,
                'producto': producto,
                'cantidad': cantidad,
                'subtotal': subtotal
            })
            total += subtotal
        except Producto.DoesNotExist:
            # Marcar producto para eliminación
            productos_a_eliminar.append(producto_id)
    
    # Eliminar productos que ya no existen
    for producto_id in productos_a_eliminar:
        del request.session['carrito'][producto_id]
    
    if productos_a_eliminar:
        request.session.modified = True
    
    context = {
        'productos_carrito': productos_carrito,
        'total': total,
        'cantidad_items': len(productos_carrito)
    }
    
    return render(request, 'productos/carrito.html', context)

@login_required
def agregar_al_carrito(request, producto_id):
    """Agregar producto al carrito"""
    if request.method == 'POST':
        producto = get_object_or_404(Producto, id=producto_id)
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
def actualizar_carrito(request):
    """Actualizar cantidad de producto en carrito via AJAX"""
    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        cantidad = int(request.POST.get('cantidad', 1))
        
        producto = get_object_or_404(Producto, id=producto_id)
        
        # Verificar stock
        if cantidad > producto.stock:
            return JsonResponse({
                'success': False, 
                'message': f'Solo hay {producto.stock} unidades disponibles'
            })
        
        # Actualizar carrito
        carrito = request.session.get('carrito', {})
        if cantidad > 0:
            carrito[str(producto_id)] = cantidad
        else:
            carrito.pop(str(producto_id), None)
        
        request.session['carrito'] = carrito
        request.session.modified = True
        
        # Calcular nuevo total
        total = 0
        for pid, cant in carrito.items():
            try:
                prod = Producto.objects.get(id=pid)
                total += prod.precio * cant
            except Producto.DoesNotExist:
                pass
        
        return JsonResponse({
            'success': True,
            'total': float(total),
            'subtotal': float(producto.precio * cantidad) if cantidad > 0 else 0
        })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

@login_required
def eliminar_del_carrito(request, producto_id):
    """Eliminar producto del carrito"""
    carrito = request.session.get('carrito', {})
    
    if str(producto_id) in carrito:
        producto = get_object_or_404(Producto, id=producto_id)
        del carrito[str(producto_id)]
        request.session['carrito'] = carrito
        request.session.modified = True
        messages.success(request, f'{producto.nombre} eliminado del carrito')
    
    return redirect('ver_carrito')

@login_required
def vaciar_carrito(request):
    """Vaciar todo el carrito"""
    request.session['carrito'] = {}
    request.session.modified = True
    messages.success(request, 'Carrito vaciado')
    return redirect('ver_carrito')

@login_required
def carrito_api(request):
    """API para obtener contenido del carrito via AJAX"""
    if request.method == 'GET':
        carrito = request.session.get('carrito', {})
        productos_carrito = []
        total = 0
        
        for producto_id, cantidad in carrito.items():
            try:
                producto = Producto.objects.get(id=producto_id)
                subtotal = producto.precio * cantidad
                productos_carrito.append({
                    'id': producto.id,
                    'nombre': producto.nombre,
                    'precio': float(producto.precio),
                    'cantidad': cantidad,
                    'subtotal': float(subtotal),
                    'imagen': producto.imagen.url if producto.imagen else None
                })
                total += subtotal
            except Producto.DoesNotExist:
                continue
        
        return JsonResponse({
            'success': True,
            'productos': productos_carrito,
            'total': float(total),
            'cantidad_items': len(productos_carrito)
        })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})
