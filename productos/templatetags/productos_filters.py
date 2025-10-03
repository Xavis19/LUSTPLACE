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