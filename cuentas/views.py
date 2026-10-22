from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render

from .forms import FormularioInicioSesion


class IniciarSesionView(LoginView):
    """HU-01: el usuario inicia sesión con su usuario y contraseña."""

    template_name = 'cuentas/iniciar_sesion.html'
    authentication_form = FormularioInicioSesion
    redirect_authenticated_user = True


@login_required
def inicio(request):
    """Menú principal. Las opciones cambian según el rol del usuario."""
    return render(request, 'cuentas/inicio.html')
