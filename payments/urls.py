from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('pago/', views.pago, name='pago'),
    path('success/', views.payment_success, name='success'),
    path('cancel/', views.payment_cancel, name='cancel'),
]