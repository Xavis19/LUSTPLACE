from django.db import models

# ✅ SI QUIERES USAR MODELOS PARA CARRITO (OPCIONAL):
# from django.contrib.auth.models import User
# from productos.models import Producto
# 
# class Carrito(models.Model):
#     usuario = models.OneToOneField(User, on_delete=models.CASCADE)
#     fecha_creacion = models.DateTimeField(auto_now_add=True)
#     
#     def __str__(self):
#         return f"Carrito de {self.usuario.username}"
# 
# class ItemCarrito(models.Model):
#     carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
#     producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
#     cantidad = models.PositiveIntegerField(default=1)
#     fecha_agregado = models.DateTimeField(auto_now_add=True)
#     
#     def __str__(self):
#         return f"{self.cantidad}x {self.producto.nombre}"
#     
#     @property
#     def subtotal(self):
#         return self.producto.precio * self.cantidad

# ✅ POR AHORA MANTENERLO VACÍO (usando sesiones)
