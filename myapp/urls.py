from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('clientes/crear/', views.crear_cliente, name='crear_cliente'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('sucursales/crear/', views.crear_sucursal, name='crear_sucursal'),
    path('vendedores/crear/', views.crear_vendedor, name='crear_vendedor'),
    path('buscar/', views.buscar_resultados, name='buscar_resultados'),
]