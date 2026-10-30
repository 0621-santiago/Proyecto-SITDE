from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('iniciar-sesion/', views.IniciarSesionView.as_view(), name='iniciar_sesion'),
    path('registrarse/', views.registrar_usuario, name='registrar_usuario'),  # <- ¡Nueva ruta de registro!
    path('cerrar-sesion/', LogoutView.as_view(), name='cerrar_sesion'),
]