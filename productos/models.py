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
    
    # 🔥 IMÁGENES DEL PRODUCTO
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True, help_text="Imagen principal del producto")
    imagen_2 = models.ImageField(upload_to='productos/', blank=True, null=True, help_text="Imagen adicional 2")
    imagen_3 = models.ImageField(upload_to='productos/', blank=True, null=True, help_text="Imagen adicional 3")
    imagen_4 = models.ImageField(upload_to='productos/', blank=True, null=True, help_text="Imagen adicional 4")
    
    # Precios y stock
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    precio_oferta = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    vendidos = models.PositiveIntegerField(default=0, help_text="Cantidad de unidades vendidas")
    
    # 🆕 CAMPOS PARA TALLAS Y COLORES
    tiene_tallas = models.BooleanField(default=False, help_text="Marcar si este producto requiere selección de talla")
    tallas_disponibles = models.CharField(max_length=200, blank=True, help_text="Tallas separadas por comas: S,M,L,XL")
    colores_disponibles = models.CharField(max_length=300, blank=True, help_text="Colores en formato: Rojo#FF0000,Negro#000000,Rosa#FF69B4")
    
    # Estados
    activo = models.BooleanField(default=True)
    destacado = models.BooleanField(default=False)
    nuevo = models.BooleanField(default=False)
    mas_vendido = models.BooleanField(default=False, help_text="Producto más vendido")
    
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
    
    @property
    def porcentaje_stock_vendido(self):
        """Calcula el porcentaje de stock vendido"""
        total = self.stock + self.vendidos
        if total == 0:
            return 0
        return round((self.vendidos / total) * 100)
    
    @property
    def imagenes_galeria(self):
        """Retorna lista de todas las imágenes disponibles para la galería"""
        imagenes = []
        if self.imagen:
            imagenes.append(self.imagen)
        if self.imagen_2:
            imagenes.append(self.imagen_2)
        if self.imagen_3:
            imagenes.append(self.imagen_3)
        if self.imagen_4:
            imagenes.append(self.imagen_4)
        return imagenes
    
    def get_colores_lista(self):
        """Retorna lista de diccionarios con nombre y código hex de colores"""
        if not self.colores_disponibles:
            return []
        colores = []
        for color in self.colores_disponibles.split(','):
            if '#' in color:
                partes = color.split('#')
                colores.append({
                    'nombre': partes[0].strip(),
                    'hex': f"#{partes[1].strip()}"
                })
        return colores

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


class Resena(models.Model):
    """Modelo para reseñas y calificaciones de productos"""
    
    CALIFICACIONES = [
        (1, '⭐ Muy malo'),
        (2, '⭐⭐ Malo'),
        (3, '⭐⭐⭐ Regular'),
        (4, '⭐⭐⭐⭐ Bueno'),
        (5, '⭐⭐⭐⭐⭐ Excelente'),
    ]
    
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='resenas')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resenas')
    calificacion = models.PositiveSmallIntegerField(choices=CALIFICACIONES, help_text="Calificación de 1 a 5 estrellas")
    titulo = models.CharField(max_length=200, blank=True, help_text="Título breve de la reseña")
    comentario = models.TextField(help_text="Comentario detallado sobre el producto")
    
    # Verificación
    compra_verificada = models.BooleanField(default=False, help_text="Usuario compró el producto")
    aprobado = models.BooleanField(default=False, help_text="Reseña aprobada por admin")
    
    # Utilidad
    votos_utiles = models.PositiveIntegerField(default=0, help_text="Votos de utilidad")
    votos_no_utiles = models.PositiveIntegerField(default=0)
    
    # Fechas
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['usuario', 'producto']  # Un usuario solo puede dejar una reseña por producto
        ordering = ['-fecha_publicacion']
        verbose_name = "Reseña"
        verbose_name_plural = "Reseñas"
    
    def __str__(self):
        return f"{self.usuario.username} - {self.producto.nombre} ({self.calificacion}⭐)"
    
    @property
    def porcentaje_utilidad(self):
        """Calcula el porcentaje de utilidad de la reseña"""
        total = self.votos_utiles + self.votos_no_utiles
        if total == 0:
            return 0
        return round((self.votos_utiles / total) * 100)


class Promocion(models.Model):
    """Modelo para promociones con carrusel"""
    
    TIPO_CHOICES = [
        ('descuento', '💰 Descuento Porcentual'),
        ('oferta', '🔥 Oferta Especial'),
        ('bundle', '📦 Pack/Bundle'),
        ('temporada', '🎯 Promoción Temporal'),
        ('flash', '⚡ Flash Sale'),
        ('nueva_coleccion', '✨ Nueva Colección'),
    ]
    
    POSICION_CHOICES = [
        ('hero', '🌟 Hero Principal'),
        ('secundaria', '⭐ Secundaria'),
        ('lateral', '📌 Lateral'),
    ]

    # Información básica
    titulo = models.CharField(max_length=200, help_text="Título llamativo de la promoción")
    subtitulo = models.CharField(max_length=300, blank=True, help_text="Subtítulo opcional")
    descripcion = models.TextField(help_text="Descripción detallada de la promoción")
    
    # Tipo y categorización
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='descuento')
    posicion = models.CharField(max_length=15, choices=POSICION_CHOICES, default='secundaria')
    
    # Imágenes
    imagen_principal = models.ImageField(
        upload_to='promociones/', 
        help_text="Imagen principal del carrusel (recomendado: 1200x600px)"
    )
    imagen_mobile = models.ImageField(
        upload_to='promociones/mobile/', 
        blank=True, null=True,
        help_text="Imagen optimizada para móvil (opcional: 800x600px)"
    )
    
    # Productos relacionados
    productos = models.ManyToManyField(
        Producto, 
        related_name='promociones', 
        blank=True,
        help_text="Productos incluidos en la promoción"
    )
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.SET_NULL, 
        null=True, blank=True,
        help_text="Categoría de la promoción (opcional)"
    )
    
    # Descuentos y precios
    descuento_porcentaje = models.DecimalField(
        max_digits=5, decimal_places=2, 
        default=0, 
        validators=[MinValueValidator(0)],
        help_text="Porcentaje de descuento (ej: 25.50 para 25.5%)"
    )
    precio_especial = models.DecimalField(
        max_digits=10, decimal_places=2, 
        blank=True, null=True,
        help_text="Precio especial fijo (opcional)"
    )
    
    # URL y enlaces
    url_personalizada = models.URLField(
        blank=True, 
        help_text="URL personalizada para la promoción (opcional)"
    )
    boton_texto = models.CharField(
        max_length=50, 
        default="Ver Promoción",
        help_text="Texto del botón CTA"
    )
    
    # Fechas y activación
    fecha_inicio = models.DateTimeField(help_text="Fecha de inicio de la promoción")
    fecha_fin = models.DateTimeField(help_text="Fecha de finalización de la promoción")
    activa = models.BooleanField(default=True, help_text="¿Promoción activa?")
    
    # Meta información
    orden = models.PositiveIntegerField(
        default=0, 
        help_text="Orden de aparición en el carrusel (menor = primero)"
    )
    vista_conteo = models.PositiveIntegerField(default=0, help_text="Número de vistas")
    click_conteo = models.PositiveIntegerField(default=0, help_text="Número de clicks")
    
    # Campos de auditoría
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    # Configuración anime/neón
    color_primary = models.CharField(
        max_length=7, 
        default="#ff0080",
        help_text="Color primario en hex (ej: #ff0080)"
    )
    color_secondary = models.CharField(
        max_length=7, 
        default="#8000ff",
        help_text="Color secundario en hex (ej: #8000ff)"
    )
    efecto_glow = models.BooleanField(default=True, help_text="Activar efecto glow neón")
    animacion_tipo = models.CharField(
        max_length=20,
        choices=[
            ('none', 'Sin animación'),
            ('fade', 'Fade suave'),
            ('slide', 'Deslizar'),
            ('zoom', 'Zoom'),
            ('bounce', 'Rebote'),
            ('glow', 'Glow pulsante'),
        ],
        default='fade'
    )

    class Meta:
        ordering = ['orden', '-fecha_creacion']
        verbose_name = "Promoción"
        verbose_name_plural = "Promociones"
        indexes = [
            models.Index(fields=['activa', 'fecha_inicio', 'fecha_fin']),
            models.Index(fields=['orden']),
            models.Index(fields=['tipo']),
        ]

    def __str__(self):
        estado = "🟢" if self.esta_activa else "🔴"
        return f"{estado} {self.titulo} ({self.get_tipo_display()})"

    @property
    def esta_activa(self):
        """Verifica si la promoción está activa y en fechas válidas"""
        from django.utils import timezone
        ahora = timezone.now()
        return (
            self.activa and 
            self.fecha_inicio <= ahora <= self.fecha_fin
        )
    
    @property
    def dias_restantes(self):
        """Calcula días restantes de la promoción"""
        from django.utils import timezone
        if not self.esta_activa:
            return 0
        delta = self.fecha_fin - timezone.now()
        return max(0, delta.days)
    
    @property
    def ctr(self):
        """Calcula el Click Through Rate"""
        if self.vista_conteo == 0:
            return 0
        return (self.click_conteo / self.vista_conteo) * 100
    
    def incrementar_vista(self):
        """Incrementa el contador de vistas"""
        self.vista_conteo += 1
        self.save(update_fields=['vista_conteo'])
    
    def incrementar_click(self):
        """Incrementa el contador de clicks"""
        self.click_conteo += 1
        self.save(update_fields=['click_conteo'])
    
    def get_url_destino(self):
        """Retorna la URL de destino de la promoción"""
        if self.url_personalizada:
            return self.url_personalizada
        elif self.productos.exists():
            # Si tiene productos, ir al primero
            return self.productos.first().get_absolute_url()
        elif self.categoria:
            # Si tiene categoría, ir a la categoría
            return f"/productos/categoria/{self.categoria.slug}/"
        else:
            # Por defecto ir a productos
            return "/productos/"
    
    def save(self, *args, **kwargs):
        # Auto-generar fechas si no se proporcionan
        if not self.fecha_inicio:
            from django.utils import timezone
            self.fecha_inicio = timezone.now()
        
        if not self.fecha_fin and self.fecha_inicio:
            from datetime import timedelta
            self.fecha_fin = self.fecha_inicio + timedelta(days=30)
            
        super().save(*args, **kwargs)


class PromocionView(models.Model):
    """Modelo para trackear vistas de promociones"""
    promocion = models.ForeignKey(Promocion, on_delete=models.CASCADE, related_name='vistas_detalle')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Vista de Promoción"
        verbose_name_plural = "Vistas de Promociones"
        indexes = [
            models.Index(fields=['promocion', 'timestamp']),
            models.Index(fields=['ip_address']),
        ]
    
    def __str__(self):
        usuario = self.usuario.username if self.usuario else 'Anónimo'
        return f"{self.promocion.titulo} - {usuario} - {self.timestamp.strftime('%d/%m/%Y %H:%M')}"


# ✅ MODELOS PARA DIRECCIONES DE ENVÍO
class DireccionEnvio(models.Model):
    """Direcciones de envío del usuario"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='direcciones')
    
    # Información de dirección
    nombre_completo = models.CharField(max_length=100, help_text="Nombre del destinatario")
    telefono = models.CharField(max_length=20)
    pais = models.CharField(max_length=50, default='Ecuador')
    provincia = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=50)
    direccion_linea1 = models.CharField(max_length=200, help_text="Calle principal")
    direccion_linea2 = models.CharField(max_length=200, blank=True, help_text="Apartamento, suite, etc.")
    codigo_postal = models.CharField(max_length=10)
    
    # Configuraciones
    es_principal = models.BooleanField(default=False, help_text="Dirección principal para envíos")
    activa = models.BooleanField(default=True)
    
    # Metadatos
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Dirección de Envío"
        verbose_name_plural = "Direcciones de Envío"
        ordering = ['-es_principal', '-fecha_actualizacion']
    
    def __str__(self):
        return f"{self.nombre_completo} - {self.ciudad}, {self.provincia}"
    
    def get_direccion_completa(self):
        lineas = [self.direccion_linea1]
        if self.direccion_linea2:
            lineas.append(self.direccion_linea2)
        lineas.extend([f"{self.ciudad}, {self.provincia}", f"{self.pais} {self.codigo_postal}"])
        return "\n".join(lineas)


# ✅ FACTURAS MANEJADAS EN authentication.models CON JSON

