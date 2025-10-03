from django.contrib import admin, messages
from django.utils.html import format_html
from .models import Categoria, Producto, ImagenProducto, Orden, ItemOrden, Promocion, PromocionView, DireccionEnvio

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

@admin.register(Promocion)
class PromocionAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo', 'posicion', 'descuento_porcentaje', 'esta_activa', 'fecha_inicio', 'fecha_fin', 'orden', 'imagen_preview', 'activa']
    list_filter = ['activa', 'tipo', 'posicion', 'fecha_inicio', 'fecha_fin']
    search_fields = ['titulo', 'descripcion']
    list_editable = ['orden', 'activa']
    date_hierarchy = 'fecha_inicio'
    actions = ['activar_promociones', 'desactivar_promociones']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('titulo', 'subtitulo', 'descripcion', 'tipo', 'posicion')
        }),
        ('Imágenes', {
            'fields': ('imagen_principal', 'imagen_mobile')
        }),
        ('Productos y Categoría', {
            'fields': ('productos', 'categoria')
        }),
        ('Descuentos y Precios', {
            'fields': ('descuento_porcentaje', 'precio_especial')
        }),
        ('Configuración', {
            'fields': ('url_personalizada', 'boton_texto', 'orden')
        }),
        ('Fechas y Activación', {
            'fields': ('fecha_inicio', 'fecha_fin', 'activa')
        }),
        ('Estilo Anime/Neón', {
            'fields': ('color_primary', 'color_secondary', 'efecto_glow', 'animacion_tipo'),
            'classes': ('collapse',)
        }),
        ('Estadísticas', {
            'fields': ('vista_conteo', 'click_conteo'),
            'classes': ('collapse',)
        })
    )
    
    filter_horizontal = ['productos']
    readonly_fields = ['vista_conteo', 'click_conteo', 'fecha_creacion', 'fecha_actualizacion']
    
    def imagen_preview(self, obj):
        if obj.imagen_principal:
            return format_html(
                '<img src="{}" width="100" height="50" style="object-fit: cover; border-radius: 8px; border: 2px solid {};">',
                obj.imagen_principal.url,
                obj.color_primary
            )
        return "Sin imagen"
    imagen_preview.short_description = "Vista previa"
    
    def esta_activa(self, obj):
        if obj.esta_activa:
            return format_html('<span style="color: #00ff00; font-weight: bold;">🟢 Activa</span>')
        else:
            return format_html('<span style="color: #ff4444; font-weight: bold;">🔴 Inactiva</span>')
    esta_activa.short_description = "Estado"
    
    def activar_promociones(self, request, queryset):
        """Activar promociones seleccionadas"""
        updated = queryset.update(activa=True)
        self.message_user(
            request,
            f'{updated} promoción(es) activada(s) exitosamente.',
            messages.SUCCESS
        )
    activar_promociones.short_description = "✅ Activar promociones seleccionadas"
    
    def desactivar_promociones(self, request, queryset):
        """Desactivar promociones seleccionadas"""
        updated = queryset.update(activa=False)
        self.message_user(
            request,
            f'{updated} promoción(es) desactivada(s) exitosamente.',
            messages.SUCCESS
        )
    desactivar_promociones.short_description = "❌ Desactivar promociones seleccionadas"

@admin.register(PromocionView)
class PromocionViewAdmin(admin.ModelAdmin):
    list_display = ['promocion', 'usuario', 'timestamp', 'ip_address']
    list_filter = ['timestamp', 'promocion']
    search_fields = ['usuario__username', 'ip_address']
    readonly_fields = ['promocion', 'usuario', 'timestamp', 'ip_address', 'user_agent']

# Personalización del admin
# ✅ ADMIN PARA DIRECCIONES Y FACTURAS
@admin.register(DireccionEnvio)
class DireccionEnvioAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'user', 'ciudad', 'provincia', 'es_principal', 'activa']
    list_filter = ['es_principal', 'activa', 'provincia', 'pais']
    search_fields = ['nombre_completo', 'user__username', 'ciudad', 'direccion_linea1']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    fieldsets = (
        ('Información del Destinatario', {
            'fields': ('user', 'nombre_completo', 'telefono')
        }),
        ('Dirección', {
            'fields': ('pais', 'provincia', 'ciudad', 'direccion_linea1', 'direccion_linea2', 'codigo_postal')
        }),
        ('Configuraciones', {
            'fields': ('es_principal', 'activa')
        }),
        ('Metadatos', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        })
    )

# ✅ FACTURAS MANEJADAS EN authentication.admin

admin.site.site_header = "🔥 MarketPlace LUST - Administración"
admin.site.site_title = "LUST Admin"
admin.site.index_title = "Panel de Control"