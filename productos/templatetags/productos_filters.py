from django import template

register = template.Library()

@register.filter
def split(value, separator):
    """Divide un string por el separador especificado"""
    if value:
        return value.split(separator)
    return []

@register.filter
def strip(value):
    """Elimina espacios en blanco al inicio y final"""
    if value:
        return value.strip()
    return value

@register.filter
def mul(value, arg):
    """Multiplica el valor por el argumento"""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def sub(value, arg):
    """Resta el argumento del valor"""
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def add_int(value, arg):
    """Suma el argumento al valor"""
    try:
        return int(value) + int(arg)
    except (ValueError, TypeError):
        return 0