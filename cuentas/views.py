from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import Group, User
from django.shortcuts import get_object_or_404, render, redirect
from .forms import FormularioInicioSesion, FormularioRegistro


def _es_admin(user):
    return (
        user.is_authenticated
        and (user.groups.filter(name='Administradores').exists() or user.is_superuser)
    )


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
    es_admin = _es_admin(request.user)
    es_empresario = request.user.groups.filter(name='Empresarios').exists()

    print(f"DEBUG -> Usuario: {request.user.username} | es_admin: {es_admin} | es_empresario: {es_empresario}")

    contexto = {
        'es_admin': es_admin,
        'es_empresario': es_empresario,
    }
    return render(request, 'cuentas/inicio.html', contexto)


@login_required
def usuarios_roles(request):
    """Permite a administradores crear usuarios y asignar roles."""
    es_admin = _es_admin(request.user)
    if not es_admin:
        messages.error(request, 'No tienes permisos para acceder a Usuarios y roles.')
        return redirect('inicio')

    if request.method == 'POST':
        accion = request.POST.get('accion')

        if accion == 'crear_usuario':
            username = request.POST.get('username', '').strip()
            email = request.POST.get('email', '').strip()
            password = request.POST.get('password', '').strip()
            rol_nombre = request.POST.get('rol', '').strip()

            if not username or not password:
                messages.error(request, 'Debes ingresar nombre de usuario y contraseña.')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'Ese nombre de usuario ya existe.')
            else:
                nuevo_usuario = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                )
                if rol_nombre:
                    grupo, _ = Group.objects.get_or_create(name=rol_nombre)
                    nuevo_usuario.groups.add(grupo)
                messages.success(request, f"Usuario '{username}' creado correctamente.")
            return redirect('usuarios_roles')

        if accion == 'asignar_rol':
            usuario_id = request.POST.get('usuario_id')
            rol_nombre = request.POST.get('rol', '').strip()
            usuario_objetivo = get_object_or_404(User, id=usuario_id)

            usuario_objetivo.groups.clear()
            if rol_nombre:
                grupo, _ = Group.objects.get_or_create(name=rol_nombre)
                usuario_objetivo.groups.add(grupo)

            messages.success(request, f"Rol actualizado para '{usuario_objetivo.username}'.")
            return redirect('usuarios_roles')

    usuarios = User.objects.prefetch_related('groups').order_by('username')
    roles_disponibles = ['Administradores', 'Empresarios']

    return render(
        request,
        'cuentas/usuarios_roles.html',
        {
            'usuarios': usuarios,
            'roles_disponibles': roles_disponibles,
            'es_admin': es_admin,
        },
    )