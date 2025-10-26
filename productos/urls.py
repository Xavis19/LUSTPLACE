from django.urls import path
from . import views
from django.http import HttpResponse

# Vista ultra simple para test
def test_simple(request):
    return HttpResponse("<h1>🔥 SERVIDOR FUNCIONANDO</h1><p>Si ves esto, Django está OK</p>")

urlpatterns = [
    path('', views.lista_productos, name='lista_productos'),
    path('simple/', test_simple, name='test_simple'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('categoria/<slug:categoria_slug>/', views.productos_por_categoria, name='productos_por_categoria'),
    path('perfil/', views.perfil, name='perfil_usuario'),  # ✅ CORREGIDO
    
    # ✅ URLs de LOGIN/REGISTER que redirigen a authentication
    path('login/', views.redirect_to_auth_login, name='login'),
    path('register/', views.redirect_to_auth_register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # ✅ URL de PAGO
    path('pago/', views.proceso_pago, name='pago'),
    
    # ✅ URLs de FAVORITOS
    path('favoritos/', views.lista_favoritos, name='lista_favoritos'),
    path('favoritos/agregar/<int:producto_id>/', views.agregar_favorito, name='agregar_favorito'),
    path('favoritos/quitar/<int:producto_id>/', views.quitar_favorito, name='quitar_favorito'),
    path('favorito/toggle/<int:favorito_id>/', views.toggle_favorito, name='toggle_favorito'),
    path('favorito/toggle-producto/<int:producto_id>/', views.toggle_favorito_producto, name='toggle_favorito_producto'),
    
    # ✅ AJAX para filtros
    path('ajax/filtros/', views.filtros_ajax, name='filtros_ajax'),
    
    # ✅ TÉRMINOS Y CONDICIONES
    path('terminos/', views.terminos, name='terminos'),
    
    # ✅ URLs DE ADMINISTRADOR (solo staff)
    path('admin-productos/', views.admin_productos, name='admin_productos'),
    path('admin-usuarios/', views.admin_usuarios, name='admin_usuarios'),
    path('admin-productos/editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('admin-productos/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('admin-productos/crear/', views.crear_producto, name='crear_producto'),
    path('admin-usuarios/toggle-staff/<int:usuario_id>/', views.toggle_usuario_staff, name='toggle_usuario_staff'),
    path('admin-usuarios/toggle-activo/<int:usuario_id>/', views.toggle_usuario_activo, name='toggle_usuario_activo'),
    
    # ✅ URLs DE PROMOCIONES MODERNAS
    path('promociones/', views.lista_productos, name='lista'),  # Vista principal moderna
    path('promocion/<int:promocion_id>/', views.productos_promocion, name='productos_promocion'),
    path('promocion-click/', views.promocion_click, name='promocion_click'),
    
    # ✅ URLs DEL CARRITO MODERNO
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_carrito, name='agregar_carrito'),
    path('carrito/ajax/actualizar/', views.actualizar_cantidad_carrito, name='actualizar_cantidad_carrito'),
    
    # ✅ FILTROS AJAX
    path('filtros-ajax/', views.filtros_ajax, name='filtros_ajax'),
    path('carrito/ajax/eliminar/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/ajax/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    path('proceso-pago/', views.proceso_pago, name='proceso_pago'),
]