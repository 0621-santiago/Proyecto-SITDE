from django.urls import path
from . import views

urlpatterns = [
    # Rutas Empresa
    path('', views.lista_empresas, name='lista_empresas'),
    path('crear/', views.crear_empresa, name='crear_empresa'),
    path('editar/<int:pk>/', views.editar_empresa, name='editar_empresa'),
    path('eliminar/<int:pk>/', views.eliminar_empresa, name='eliminar_empresa'),

    # Rutas Producto
    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/editar/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
]