from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils.text import slugify
from PIL import Image
import uuid

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)
    imagen = models.ImageField(upload_to='categorias/', blank=True, null=True)
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.nombre)
            contador = 1
            slug_unico = base_slug
            while Categoria.objects.filter(slug=slug_unico).exists():
                slug_unico = f"{base_slug}-{contador}"
                contador += 1
            self.slug = slug_unico
        super().save(*args, **kwargs)

class Producto(models.Model):
    # Información básica
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos', null=True, blank=True)
    
    # 🔥 IMAGEN PRINCIPAL
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    
    # Precios y stock
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    precio_oferta = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    
    # 🆕 CAMPOS PARA TALLAS
    tiene_tallas = models.BooleanField(default=False, help_text="Marcar si este producto requiere selección de talla")
    tallas_disponibles = models.CharField(max_length=200, blank=True, help_text="Tallas separadas por comas: S,M,L,XL")
    
    # Estados
    activo = models.BooleanField(default=True)
    destacado = models.BooleanField(default=False)
    nuevo = models.BooleanField(default=False)
    
    # SEO - ✅ CAMPOS FALTANTES AGREGADOS
    slug = models.SlugField(unique=True, blank=True)
    meta_titulo = models.CharField(max_length=60, blank=True, help_text="Título SEO (60 caracteres máx)")
    meta_descripcion = models.CharField(max_length=160, blank=True, help_text="Descripción SEO (160 caracteres máx)")
    
    # Fechas
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        # Generar slug único
        if not self.slug:
            base_slug = slugify(self.nombre)
            contador = 1
            slug_unico = base_slug
            while Producto.objects.filter(slug=slug_unico).exclude(pk=self.pk).exists():
                slug_unico = f"{base_slug}-{contador}"
                contador += 1
            self.slug = slug_unico
        
        # Auto-generar meta_titulo si está vacío
        if not self.meta_titulo:
            self.meta_titulo = self.nombre[:60]
        
        # Auto-generar meta_descripcion si está vacía
        if not self.meta_descripcion:
            self.meta_descripcion = self.descripcion[:160]
        
        super().save(*args, **kwargs)

    @property
    def precio_final(self):
        return self.precio_oferta if self.precio_oferta else self.precio

    @property
    def tiene_descuento(self):
        return self.precio_oferta and self.precio_oferta < self.precio

    @property
    def porcentaje_descuento(self):
        if self.tiene_descuento:
            return round(((self.precio - self.precio_oferta) / self.precio) * 100)
        return 0

class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='imagenes_adicionales')
    imagen = models.ImageField(upload_to='productos/adicionales/')
    alt_text = models.CharField(max_length=200, blank=True)
    orden = models.PositiveIntegerField(default=0)
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return f"Imagen de {self.producto.nombre}"

class Orden(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('procesando', 'Procesando'),
        ('enviada', 'Enviada'),
        ('entregada', 'Entregada'),
        ('cancelada', 'Cancelada'),
    ]
    
    METODOS_PAGO = [
        ('tarjeta', 'Tarjeta de Crédito'),
        ('paypal', 'PayPal'),
        ('transferencia', 'Transferencia'),
        ('efectivo', 'Efectivo'),
    ]

    numero_orden = models.CharField(max_length=20, unique=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ordenes')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO, default='tarjeta')
    direccion_envio = models.TextField()
    notas_especiales = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Orden {self.numero_orden}"

    def save(self, *args, **kwargs):
        if not self.numero_orden:
            import random
            import string
            self.numero_orden = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        super().save(*args, **kwargs)

class ItemOrden(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre}"
    
    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario

class Favorito(models.Model):
    """Modelo para productos favoritos del usuario"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favoritos')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='favoritos')
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['usuario', 'producto']  # Un usuario no puede tener el mismo producto dos veces en favoritos
        ordering = ['-fecha_agregado']
    
    def __str__(self):
        return f"{self.usuario.username} - {self.producto.nombre}"

