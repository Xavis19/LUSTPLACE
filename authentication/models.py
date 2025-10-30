from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

class Role(models.Model):
    ROLE_CHOICES = [
        ('user', 'Usuario Normal'),
        ('admin', 'Administrador'),
    ]
    
    name = models.CharField(max_length=50, choices=ROLE_CHOICES, unique=True)
    description = models.TextField(blank=True)
    permissions = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.get_name_display()
    
    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.ForeignKey(Role, on_delete=models.SET_DEFAULT, default=1)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default='Colombia')
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    
    # ✅ NUEVOS CAMPOS PARA FACTURACIÓN
    documento_identidad = models.CharField(max_length=20, blank=True, help_text="DNI, Cédula, Pasaporte")
    tipo_documento = models.CharField(max_length=10, choices=[
        ('DNI', 'DNI'),
        ('CEDULA', 'Cédula'),
        ('PASAPORTE', 'Pasaporte'),
        ('RUC', 'RUC'),
    ], default='DNI', blank=True)
    
    # ✅ PREFERENCIAS DE MARKETING
    recibir_ofertas = models.BooleanField(default=True)
    recibir_facturas_email = models.BooleanField(default=True)
    
    # ✅ INFORMACIÓN PARA LOGIN CON GOOGLE
    google_id = models.CharField(max_length=100, blank=True, unique=True, null=True)
    provider = models.CharField(max_length=50, default='email', choices=[
        ('email', 'Email/Password'),
        ('google', 'Google'),
    ])
    google_verified = models.BooleanField(default=False, help_text="Verificado con Google OAuth")
    
    # ✅ CAMPOS ADICIONALES PARA PERFIL COMPLETO
    telefono_verificado = models.BooleanField(default=False)
    email_verificado = models.BooleanField(default=False)
    fecha_ultima_actividad = models.DateTimeField(auto_now=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.role.name}"
    
    def has_permission(self, permission_key):
        """Verificar si el usuario tiene un permiso específico"""
        return self.role.permissions.get(permission_key, False)
    
    @property
    def is_admin(self):
        return self.role.name == 'admin'
    
    def get_full_name(self):
        """Obtener nombre completo del usuario"""
        return f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username
    
    def get_direccion_principal(self):
        """Obtener la dirección principal de envío"""
        from productos.models import DireccionEnvio
        return DireccionEnvio.objects.filter(user=self.user, es_principal=True).first()
    
    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"

# ✅ SIGNALS PARA CREAR PERFIL AUTOMÁTICAMENTE
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Crea un perfil automáticamente cuando se crea un nuevo usuario"""
    if created:
        # Obtener o crear rol 'user' por defecto
        user_role, _ = Role.objects.get_or_create(
            name='user',
            defaults={
                'description': 'Usuario normal del sistema',
                'permissions': {
                    'can_buy': True,
                    'can_view_products': True,
                    'can_manage_cart': True
                }
            }
        )
        # Crear perfil con avatar por defecto
        UserProfile.objects.create(
            user=instance, 
            role=user_role,
            avatar='media/img/frank20.jpg'
        )

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Guarda el perfil cuando se actualiza el usuario"""
    if hasattr(instance, 'profile'):
        instance.profile.save()

# ✅ MODELO DE FACTURAS CON JSON
class Factura(models.Model):
    numero_factura = models.CharField(max_length=20, unique=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='facturas')
    
    # 🔥 DATOS EN JSON PARA MÁXIMA FLEXIBILIDAD
    datos_cliente = models.JSONField(default=dict, help_text="Información del cliente: nombre, email, telefono, etc.")
    datos_productos = models.JSONField(default=list, help_text="Lista de productos con detalles completos")
    datos_financieros = models.JSONField(default=dict, help_text="Subtotal, impuestos, descuentos, total")
    datos_envio = models.JSONField(default=dict, help_text="Dirección y método de envío")
    datos_adicionales = models.JSONField(default=dict, help_text="Información extra: cupones, notas, etc.")
    
    # Estados y fechas
    estado = models.CharField(max_length=20, choices=[
        ('generada', 'Generada'),
        ('enviada', 'Enviada por Email'),
        ('pagada', 'Pagada'),
        ('anulada', 'Anulada')
    ], default='generada')
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_envio = models.DateTimeField(null=True, blank=True)
    fecha_pago = models.DateTimeField(null=True, blank=True)
    
    # Archivo PDF opcional
    archivo_pdf = models.FileField(upload_to='facturas/', null=True, blank=True)
    
    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"
        ordering = ['-fecha_creacion']
    
    def save(self, *args, **kwargs):
        if not self.numero_factura:
            # Generar número de factura único
            import datetime
            fecha = datetime.datetime.now()
            self.numero_factura = f"LUST-{fecha.year}{fecha.month:02d}{fecha.day:02d}-{fecha.hour:02d}{fecha.minute:02d}{fecha.second:02d}"
        super().save(*args, **kwargs)
    
    @property
    def total(self):
        """Obtener total desde los datos JSON"""
        return self.datos_financieros.get('total', 0)
    
    @property
    def cliente_email(self):
        """Obtener email del cliente desde los datos JSON"""
        return self.datos_cliente.get('email', '')
    
    @property
    def cliente_nombre(self):
        """Obtener nombre del cliente desde los datos JSON"""
        return self.datos_cliente.get('nombre', 'Sin nombre')
    
    def __str__(self):
        return f"Factura {self.numero_factura} - {self.cliente_nombre}"
