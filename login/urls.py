from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.login_view, name='login_form'),  # ✅ Para /admin/
    path('register/', views.registro_view, name='register_form'),  # ✅ Para /admin/register/
    path('logout/', LogoutView.as_view(next_page='lista_productos'), name='logout_form'),
]