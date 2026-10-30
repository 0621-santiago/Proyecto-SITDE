from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from .forms import FormularioInicioSesion, FormularioRegistro


class IniciarSesionView(LoginView):
    """HU-01: El usuario inicia sesión con su usuario y contraseña."""
    template_name = 'cuentas/iniciar_sesion.html'
    authentication_form = FormularioInicioSesion
    redirect_authenticated_user = True

    def form_invalid(self, form):
        messages.error(self.request, 'Usuario o contraseña incorrectos. Por favor, verifica tus datos.')
        return super().form_invalid(form)


def registrar_usuario(request):
    """Vista para el registro de nuevos usuarios en el sistema."""
    if request.user.is_authenticated:
        return redirect('inicio')

    if request.method == 'POST':
        form = FormularioRegistro(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Asignar automáticamente el rol de Empresario
            grupo_empresario, _ = Group.objects.get_or_create(name='Empresarios')
            user.groups.add(grupo_empresario)

            # Iniciar sesión automáticamente después de registrarse
            login(request, user)
            messages.success(request, f'¡Cuenta creada con éxito! Bienvenido, {user.first_name or user.username}.')
            return redirect('inicio')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = FormularioRegistro()

    return render(request, 'cuentas/registrar.html', {'form': form})


@login_required
def inicio(request):
    """Menú principal. Las opciones cambian según el rol del usuario."""
    es_admin = request.user.groups.filter(name='Administradores').exists() or request.user.is_superuser
    es_empresario = request.user.groups.filter(name='Empresarios').exists()

    # Esto imprimirá en tu terminal de VS Code qué rol tiene el usuario conectado
    print(f"DEBUG -> Usuario: {request.user.username} | es_admin: {es_admin} | es_empresario: {es_empresario}")

    contexto = {
        'es_admin': es_admin,
        'es_empresario': es_empresario,
    }
    return render(request, 'cuentas/inicio.html', contexto)