from django.contrib import admin
from django.utils.html import format_html
from .models import Categoria, Producto, ImagenProducto, Orden, ItemOrden

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activa', 'fecha_creacion', 'imagen_preview']
    list_filter = ['activa', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    prepopulated_fields = {'slug': ('nombre',)}
    
    def imagen_preview(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;">', obj.imagen.url)
        return "Sin imagen"
    imagen_preview.short_description = "Vista previa"

class ImagenProductoInline(admin.TabularInline):
    model = ImagenProducto
    extra = 1
    fields = ['imagen', 'alt_text', 'orden', 'activa', 'imagen_preview']
    readonly_fields = ['imagen_preview']
    
    def imagen_preview(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" width="80" height="80" style="object-fit: cover; border-radius: 4px;">', obj.imagen.url)
        return "Sin imagen"
    imagen_preview.short_description = "Vista previa"

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'precio_final', 'stock', 'activo', 'destacado', 'imagen_preview']
    list_filter = ['activo', 'destacado', 'nuevo', 'categoria', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion', 'meta_titulo']
    prepopulated_fields = {'slug': ('nombre',)}
    list_editable = ['activo', 'destacado', 'stock']
    inlines = [ImagenProductoInline]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion', 'categoria', 'imagen')
        }),
        ('Precios y Stock', {
            'fields': ('precio', 'precio_oferta', 'stock')
        }),
        ('Estados', {
            'fields': ('activo', 'destacado', 'nuevo')
        }),
        ('SEO', {
            'fields': ('slug', 'meta_titulo', 'meta_descripcion'),
            'classes': ('collapse',)
        }),
    )
    
    def imagen_preview(self, obj):
        if obj.imagen:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit: cover; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">',
                obj.imagen.url
            )
        return format_html('<div style="width: 60px; height: 60px; background: #f0f0f0; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 12px; color: #666;">Sin imagen</div>')
    imagen_preview.short_description = "Imagen"

class ItemOrdenInline(admin.TabularInline):
    model = ItemOrden
    extra = 0
    readonly_fields = ['subtotal']

@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ['numero_orden', 'usuario', 'total', 'estado', 'fecha_creacion']
    list_filter = ['estado', 'metodo_pago', 'fecha_creacion']
    search_fields = ['numero_orden', 'usuario__username', 'usuario__email']
    readonly_fields = ['numero_orden', 'fecha_creacion', 'fecha_actualizacion']
    inlines = [ItemOrdenInline]
    
    fieldsets = (
        ('Información de la Orden', {
            'fields': ('numero_orden', 'usuario', 'estado', 'metodo_pago')
        }),
        ('Detalles Financieros', {
            'fields': ('total',)
        }),
        ('Envío', {
            'fields': ('direccion_envio', 'notas_especiales')
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

# Personalización del admin
admin.site.site_header = "🔥 MarketPlace LUST - Administración"
admin.site.site_title = "LUST Admin"
admin.site.index_title = "Panel de Control"