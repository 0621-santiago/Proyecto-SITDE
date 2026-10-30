from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Empresa, Producto
from .forms import EmpresaForm, ProductoForm

# --- VISTAS DE EMPRESA ---

@login_required
def lista_empresas(request):
    es_admin = request.user.groups.filter(name='Administradores').exists() or request.user.is_superuser
    
    # Si un empresario intenta ingresar por URL, lo redirigimos directo a productos
    if not es_admin:
        return redirect('lista_productos')
        
    empresas = Empresa.objects.all()
    return render(request, 'inventario/lista_empresas.html', {'empresas': empresas, 'es_admin': es_admin})

@login_required
def crear_empresa(request):
    es_admin = request.user.groups.filter(name='Administradores').exists() or request.user.is_superuser
    if not es_admin:
        messages.error(request, "No tienes permisos para registrar empresas.")
        return redirect('lista_productos')

    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_empresas')
    else:
        form = EmpresaForm()
    return render(request, 'inventario/crear_empresa.html', {'form': form})

@login_required
def editar_empresa(request, pk):
    es_admin = request.user.groups.filter(name='Administradores').exists() or request.user.is_superuser
    if not es_admin:
        messages.error(request, "No tienes permisos para editar empresas.")
        return redirect('lista_productos')

    empresa = get_object_or_404(Empresa, pk=pk)
    if request.method == 'POST':
        form = EmpresaForm(request.POST, instance=empresa)
        if form.is_valid():
            form.save()
            return redirect('lista_empresas')
    else:
        form = EmpresaForm(instance=empresa)
    return render(request, 'inventario/crear_empresa.html', {'form': form, 'es_edicion': True})

@login_required
def eliminar_empresa(request, pk):
    es_admin = request.user.groups.filter(name='Administradores').exists() or request.user.is_superuser
    if not es_admin:
        messages.error(request, "No tienes permisos para eliminar empresas.")
        return redirect('lista_productos')
        
    empresa = get_object_or_404(Empresa, pk=pk)
    if request.method == 'POST':
        empresa.delete()
        return redirect('lista_empresas')
    return render(request, 'inventario/confirmar_eliminar.html', {'objeto': empresa})


# --- VISTAS DE PRODUCTO ---

@login_required
def lista_productos(request):
    es_admin = request.user.groups.filter(name='Administradores').exists() or request.user.is_superuser
    productos = Producto.objects.all()
    return render(request, 'inventario/lista_productos.html', {
        'productos': productos,
        'es_admin': es_admin
    })

@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'inventario/crear_producto.html', {'form': form})

@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'inventario/crear_producto.html', {'form': form, 'es_edicion': True})

@login_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('lista_productos')
    return render(request, 'inventario/confirmar_eliminar.html', {'objeto': producto})