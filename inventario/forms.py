from django import forms
from .models import Empresa, Producto

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nombre', 'nit', 'municipio']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la empresa'}),
            'nit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'NIT'}),
            'municipio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Municipio'}),
        }


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'stock', 'proveedor'] # O 'empresa' según tu modelo
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad inicial'}),
            'proveedor': forms.Select(attrs={'class': 'form-control'}),
        }