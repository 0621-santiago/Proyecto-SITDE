from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

class FormularioInicioSesion(AuthenticationForm):
    """Formulario de inicio de sesión con mensajes en español (HU-01)."""

    error_messages = {
        'invalid_login': 'Usuario o contraseña incorrectos. Intente nuevamente.',
        'inactive': 'Esta cuenta está inactiva. Comuníquese con el administrador.',
    }

    username = forms.CharField(
        label='Usuario',
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'autocomplete': 'username',
            'placeholder': 'Ingrese su usuario',
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        label='Contraseña',
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'placeholder': '••••••••',
            'class': 'form-control'
        }),
    )


class FormularioRegistro(UserCreationForm):
    """Formulario para el registro de nuevos usuarios."""

    first_name = forms.CharField(
        label='Nombre',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ingrese su nombre',
            'class': 'form-control',
            'autocomplete': 'given-name'
        })
    )
    last_name = forms.CharField(
        label='Apellido',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ingrese su apellido',
            'class': 'form-control',
            'autocomplete': 'family-name'
        })
    )
    email = forms.EmailField(
        label='Correo electrónico',
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'ejemplo@correo.com',
            'class': 'form-control',
            'autocomplete': 'email'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Nombre de usuario',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Ingrese un usuario',
            'class': 'form-control',
            'autocomplete': 'username'
        })
        # Estilizado para los campos de contraseña nativos de UserCreationForm
        if 'password1' in self.fields:
            self.fields['password1'].widget.attrs.update({
                'placeholder': '••••••••',
                'class': 'form-control'
            })
        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs.update({
                'placeholder': 'Repita su contraseña',
                'class': 'form-control'
            })