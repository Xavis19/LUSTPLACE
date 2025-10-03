from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from .models import Role, UserProfile, Factura

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'get_permissions_count']
    search_fields = ['name', 'description']
    
    def get_permissions_count(self, obj):
        return len(obj.permissions) if obj.permissions else 0
    get_permissions_count.short_description = "Permisos"

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'phone', 'birth_date', 'is_admin', 'created_at']
    list_filter = ['role', 'provider', 'recibir_ofertas', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone', 'documento_identidad']
    readonly_fields = ['created_at', 'updated_at', 'google_id']
    
    fieldsets = (
        ('Usuario', {
            'fields': ('user', 'role')
        }),
        ('Información Personal', {
            'fields': ('phone', 'birth_date', 'documento_identidad', 'tipo_documento', 'address', 'city', 'country')
        }),
        ('Avatar', {
            'fields': ('avatar',)
        }),
        ('Configuraciones', {
            'fields': ('recibir_ofertas', 'recibir_facturas_email', 'is_verified')
        }),
        ('Autenticación', {
            'fields': ('provider', 'google_id', 'last_login_ip'),
            'classes': ('collapse',)
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ['numero_factura', 'get_cliente_nombre', 'usuario', 'get_total', 'estado', 'fecha_creacion', 'fecha_envio']
    list_filter = ['estado', 'fecha_creacion', 'fecha_envio']
    search_fields = ['numero_factura', 'usuario__username']
    readonly_fields = ['numero_factura', 'fecha_creacion', 'fecha_envio', 'fecha_pago']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('numero_factura', 'usuario', 'estado')
        }),
        ('Datos del Cliente (JSON)', {
            'fields': ('datos_cliente',),
            'description': 'Información del cliente almacenada en formato JSON'
        }),
        ('Productos (JSON)', {
            'fields': ('datos_productos',),
            'description': 'Lista de productos con detalles completos'
        }),
        ('Financieros (JSON)', {
            'fields': ('datos_financieros',),
            'description': 'Subtotal, impuestos, descuentos, total'
        }),
        ('Envío (JSON)', {
            'fields': ('datos_envio',),
            'description': 'Dirección y método de envío'
        }),
        ('Adicionales (JSON)', {
            'fields': ('datos_adicionales',),
            'description': 'Cupones, notas, información extra',
            'classes': ('collapse',)
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_envio', 'fecha_pago'),
            'classes': ('collapse',)
        }),
        ('Archivos', {
            'fields': ('archivo_pdf',),
            'classes': ('collapse',)
        })
    )
    
    actions = ['generar_pdf', 'enviar_por_email', 'marcar_como_pagada']
    
    def get_cliente_nombre(self, obj):
        return obj.cliente_nombre
    get_cliente_nombre.short_description = "Cliente"
    
    def get_total(self, obj):
        total = obj.total
        return format_html('<strong style="color: #28a745;">${}</strong>', total)
    get_total.short_description = "Total"
    
    def generar_pdf(self, request, queryset):
        # TODO: Implementar generación de PDF
        self.message_user(request, f"Función de PDF pendiente para {queryset.count()} facturas.")
    generar_pdf.short_description = "Generar PDF"
    
    def enviar_por_email(self, request, queryset):
        # TODO: Implementar envío por email
        self.message_user(request, f"Función de email pendiente para {queryset.count()} facturas.")
    enviar_por_email.short_description = "Enviar por Email"
    
    def marcar_como_pagada(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(estado='pagada', fecha_pago=timezone.now())
        self.message_user(request, f"{updated} facturas marcadas como pagadas.")
    marcar_como_pagada.short_description = "Marcar como Pagada"

# Personalización del admin
admin.site.site_header = "🔥 MarketPlace LUST - Administración"
admin.site.site_title = "LUST Admin"
admin.site.index_title = "Panel de Control"
