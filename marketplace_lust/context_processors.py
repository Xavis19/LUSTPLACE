"""
Context processors para LUSTPLACE
"""

def carrito_context(request):
    """
    Context processor para mostrar información del carrito en todos los templates
    """
    carrito = request.session.get('carrito', {})
    
    # Calcular total de items (suma de cantidades)
    total_items = sum(carrito.values()) if carrito else 0
    
    # Calcular cantidad de productos únicos
    productos_unicos = len(carrito) if carrito else 0
    
    return {
        'carrito_total_items': total_items,
        'carrito_productos_unicos': productos_unicos,
        'carrito_tiene_productos': total_items > 0
    }
