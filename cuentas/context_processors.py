from .roles import ADMINISTRADOR, obtener_rol


def rol_usuario(request):
    """Deja el rol del usuario disponible en todas las plantillas."""
    rol = obtener_rol(request.user) if hasattr(request, 'user') else None
    return {'rol_usuario': rol, 'es_administrador': rol == ADMINISTRADOR}
