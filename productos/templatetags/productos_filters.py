"""
Filtros y tags personalizados para la app productos
"""

from django import template
from decimal import Decimal

register = template.Library()


@register.filter(name='currency')
def currency(value):
    """
    Formatea un número como moneda
    Uso: {{ producto.precio|currency }}
    Resultado: $99.99
    """
    if value is None:
        return "$0.00"
    
    try:
        value = Decimal(str(value))
        return f"${value:,.2f}"
    except (ValueError, TypeError):
        return "$0.00"


@register.filter(name='multiply')
def multiply(value, arg):
    """
    Multiplica dos valores
    Uso: {{ precio|multiply:cantidad }}
    """
    try:
        return Decimal(str(value)) * Decimal(str(arg))
    except (ValueError, TypeError):
        return 0


@register.filter(name='mul')
def mul(value, arg):
    """
    Alias de multiply - Multiplica dos valores
    Uso: {{ forloop.counter0|mul:50 }}
    """
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0


@register.filter(name='percentage')
def percentage(value):
    """
    Formatea un número como porcentaje
    Uso: {{ 0.15|percentage }}
    Resultado: 15%
    """
    if value is None:
        return "0%"
    
    try:
        value = float(value)
        if value < 1:  # Si es decimal (0.15)
            value = value * 100
        return f"{value:.0f}%"
    except (ValueError, TypeError):
        return "0%"


@register.filter(name='stock_status')
def stock_status(stock):
    """
    Retorna el estado del stock
    Uso: {{ producto.stock|stock_status }}
    """
    if stock == 0:
        return "Agotado"
    elif stock < 5:
        return "Últimas unidades"
    elif stock < 10:
        return "Pocas unidades"
    else:
        return "Disponible"


@register.filter(name='stars')
def stars(calificacion):
    """
    Convierte un número en estrellas
    Uso: {{ producto.calificacion|stars }}
    Resultado: ★★★★☆
    """
    if not calificacion:
        return "☆☆☆☆☆"
    
    try:
        calificacion = int(calificacion)
        filled = "★" * calificacion
        empty = "☆" * (5 - calificacion)
        return filled + empty
    except (ValueError, TypeError):
        return "☆☆☆☆☆"


@register.simple_tag
def calculate_discount(precio_original, precio_oferta):
    """
    Calcula el porcentaje de descuento
    Uso: {% calculate_discount producto.precio producto.precio_oferta %}
    """
    if not precio_original or not precio_oferta:
        return 0
    
    try:
        precio_original = Decimal(str(precio_original))
        precio_oferta = Decimal(str(precio_oferta))
        
        if precio_original <= precio_oferta:
            return 0
        
        descuento = ((precio_original - precio_oferta) / precio_original) * 100
        return round(descuento)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0


@register.filter(name='get_range')
def get_range(value):
    """
    Retorna un rango para iterar en templates
    Uso: {% for i in 5|get_range %}
    """
    try:
        return range(int(value))
    except (ValueError, TypeError):
        return range(0)


@register.filter(name='split')
def split(value, separator=','):
    """
    Divide una cadena
    Uso: {{ "rojo,azul,verde"|split:"," }}
    """
    if not value:
        return []
    return str(value).split(separator)


@register.filter(name='truncate_chars')
def truncate_chars(value, max_length=100):
    """
    Trunca un texto a un número máximo de caracteres
    Uso: {{ producto.descripcion|truncate_chars:150 }}
    """
    if not value:
        return ""
    
    value = str(value)
    if len(value) <= max_length:
        return value
    
    return value[:max_length].rsplit(' ', 1)[0] + '...'


@register.filter(name='badge_class')
def badge_class(value):
    """
    Retorna la clase CSS para un badge según el estado
    Uso: {{ producto.stock|badge_class }}
    """
    try:
        stock = int(value)
        if stock == 0:
            return "badge-danger"
        elif stock < 5:
            return "badge-warning"
        else:
            return "badge-success"
    except (ValueError, TypeError):
        return "badge-secondary"


@register.filter(name='add_class')
def add_class(field, css_class):
    """
    Agrega una clase CSS a un campo de formulario
    Uso: {{ form.nombre|add_class:"form-control" }}
    """
    return field.as_widget(attrs={"class": css_class})


@register.filter(name='default_if_none')
def default_if_none(value, default="N/A"):
    """
    Retorna un valor por defecto si es None
    Uso: {{ producto.descripcion|default_if_none:"Sin descripción" }}
    """
    return value if value is not None else default


@register.inclusion_tag('productos/partials/precio_badge.html')
def precio_badge(producto):
    """
    Tag de inclusión para mostrar el badge de precio
    Uso: {% precio_badge producto %}
    """
    tiene_descuento = producto.precio_oferta and producto.precio_oferta < producto.precio
    
    context = {
        'producto': producto,
        'tiene_descuento': tiene_descuento,
        'precio_final': producto.precio_oferta if tiene_descuento else producto.precio,
    }
    
    if tiene_descuento:
        descuento = ((producto.precio - producto.precio_oferta) / producto.precio) * 100
        context['porcentaje_descuento'] = round(descuento)
    
    return context


@register.simple_tag
def get_color_name(hex_color):
    """
    Retorna el nombre de un color desde su código hex
    Uso: {% get_color_name "#FF0000" %}
    """
    color_map = {
        '#FF0000': 'Rojo',
        '#000000': 'Negro',
        '#FFFFFF': 'Blanco',
        '#FF69B4': 'Rosa',
        '#0000FF': 'Azul',
        '#00FF00': 'Verde',
        '#FFFF00': 'Amarillo',
        '#FFA500': 'Naranja',
        '#800080': 'Morado',
        '#808080': 'Gris',
    }
    return color_map.get(hex_color.upper(), 'Otro')


@register.filter(name='abs')
def abs_filter(value):
    """
    Retorna el valor absoluto de un número
    Uso: {{ numero|abs }}
    """
    try:
        return abs(int(value))
    except (ValueError, TypeError):
        return 0
