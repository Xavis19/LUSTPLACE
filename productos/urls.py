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
    path('perfil/', views.perfil, name='perfil_usuario'),  # ✅ CORREGIDO
    path('api/chatbot/', views.chatbot_api, name='chatbot_api'),
    
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
]