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
    
    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"

# ✅ SIGNALS PARA CREAR PERFIL AUTOMÁTICAMENTE
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
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
        UserProfile.objects.create(user=instance, role=user_role)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
