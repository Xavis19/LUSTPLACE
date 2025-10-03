from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = 'authentication'

urlpatterns = [
    # URLs Web para login/register
    path('login/', views.web_login_view, name='web_login'),
    path('register/', views.web_register_view, name='web_register'),
    
    # APIs JWT
    path('api/register/', views.RegisterAPIView.as_view(), name='api_register'),
    path('api/login/', views.login_api_view, name='api_login'),
    path('api/logout/', views.logout_api_view, name='api_logout'),
    path('api/profile/', views.UserProfileAPIView.as_view(), name='api_profile'),
    path('api/user-info/', views.user_info_view, name='api_user_info'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]