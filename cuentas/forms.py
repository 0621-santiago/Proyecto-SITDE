from django import forms
from django.contrib.auth.forms import AuthenticationForm


class FormularioInicioSesion(AuthenticationForm):
    """Formulario de inicio de sesión con mensajes en español (HU-01)."""

    error_messages = {
        'invalid_login': 'Usuario o contraseña incorrectos. Intente nuevamente.',
        'inactive': 'Esta cuenta está inactiva. Comuníquese con el administrador.',
    }

    username = forms.CharField(
        label='Usuario',
        widget=forms.TextInput(attrs={'autofocus': True, 'autocomplete': 'username'}),
    )
    password = forms.CharField(
        label='Contraseña',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )
