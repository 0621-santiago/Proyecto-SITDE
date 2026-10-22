"""Roles del sistema SITDE.

Los roles se manejan con los Grupos de Django. La migración
0001_crear_grupos crea los dos grupos al aplicar `migrate`.
"""

ADMINISTRADOR = 'Administrador'
EMPRESARIO = 'Empresario'

ROLES = [ADMINISTRADOR, EMPRESARIO]


def obtener_rol(usuario):
    """Devuelve el rol del usuario o None si no tiene ninguno.

    Un superusuario de Django se trata como Administrador.
    """
    if not usuario.is_authenticated:
        return None
    if usuario.is_superuser or usuario.groups.filter(name=ADMINISTRADOR).exists():
        return ADMINISTRADOR
    if usuario.groups.filter(name=EMPRESARIO).exists():
        return EMPRESARIO
    return None


def es_administrador(usuario):
    return obtener_rol(usuario) == ADMINISTRADOR
