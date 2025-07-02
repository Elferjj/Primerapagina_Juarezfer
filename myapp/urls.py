from django.urls import path , include
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.home, name='inicio'),
    path('about/', views.about, name='about'),

    # URLs de Autenticación (las que usaremos con nuestras vistas)
    path('registro/', views.user_register, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('perfil/editar/', views.edit_profile, name='edit_profile'),
    path('perfil/<str:username>/', views.ver_perfil_usuario, name='ver_perfil'),
    path('perfil/<str:username>/', views.perfil_usuario, name='ver_perfil_usuario'),
    path('perfil/', views.ver_perfil_usuario, {'username': 'me'}, name='mi_perfil'),


    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('productos/publicar/', views.crear_producto, name='crear_producto'),
    path('sucursales/crear/', views.crear_sucursal, name='crear_sucursal'),      
    path('sucursales/eliminar/<int:sucursal_id>/', views.eliminar_sucursal, name='eliminar_sucursal'),

    path('productos/', views.lista_productos, name='lista_productos'), 
    path('productos/<int:pk>/', views.detalle_producto, name='detalle_producto'), 
    path('productos/<int:pk>/editar/', views.editar_producto, name='editar_producto'), 
    path('productos/<int:pk>/eliminar/', views.eliminar_producto, name='eliminar_producto'),

    path('productos/clientes/', views.lista_productos_por_cliente, name='lista_productos_por_cliente'), 
    path('sucursales/lista/', views.lista_sucursales, name='lista_sucursales'), 


    
]
