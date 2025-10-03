from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'authentication'

urlpatterns = [
    # URLs Web para login/register
    path('login/', views.web_login_view, name='web_login'),
    path('register/', views.web_register_view, name='web_register'),
    path('logout/', views.logout_view, name='logout'),
    
    # URLs Web para perfil de usuario
    path('perfil/', views.perfil_usuario_view, name='perfil_usuario'),
    path('editar-perfil/', views.editar_perfil_view, name='editar_perfil'),
    path('mis-direcciones/', views.mis_direcciones_view, name='mis_direcciones'),
    path('agregar-direccion/', views.agregar_direccion_view, name='agregar_direccion'),
    path('eliminar-direccion/<int:direccion_id>/', views.eliminar_direccion_view, name='eliminar_direccion'),
    path('mis-pedidos/', views.mis_pedidos_view, name='mis_pedidos'),
    path('mis-favoritos/', views.mis_favoritos_view, name='mis_favoritos'),
    
    # URLs AJAX
    path('ajax/cambiar-avatar/', views.cambiar_avatar_ajax, name='cambiar_avatar_ajax'),
    
    # URLs Google OAuth
    path('google-auth/', views.GoogleAuthView.as_view(), name='google_auth'),
    path('verificar-google/', views.verificar_google_view, name='verificar_google'),
    path('google-callback/', views.google_callback_view, name='google_callback'),
    
    # APIs JWT
    path('api/register/', views.RegisterAPIView.as_view(), name='api_register'),
    path('api/login/', views.login_api_view, name='api_login'),
    path('api/logout/', views.logout_api_view, name='api_logout'),
    path('api/profile/', views.UserProfileAPIView.as_view(), name='api_profile'),
    path('api/user-info/', views.user_info_view, name='api_user_info'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]