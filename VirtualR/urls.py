# filepath: VirtualR/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.prueba, name='prueba_virtualr'),
]