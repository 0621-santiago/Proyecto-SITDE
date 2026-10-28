from django.shortcuts import render, redirect, get_object_or_404
from .models import Empresa, Producto
from .forms import EmpresaForm, ProductoForm

# --- VISTAS DE EMPRESA ---
def lista_empresas(request):
    empresas = Empresa.objects.all()
    return render(request, 'inventario/lista_empresas.html', {'empresas': empresas})

def crear_empresa(request):
    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_empresas')
    else:
        form = EmpresaForm()
    return render(request, 'inventario/crear_empresa.html', {'form': form})

def editar_empresa(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk)
    if request.method == 'POST':
        form = EmpresaForm(request.POST, instance=empresa)
        if form.is_valid():
            form.save()
            return redirect('lista_empresas')
    else:
        form = EmpresaForm(instance=empresa)
    return render(request, 'inventario/crear_empresa.html', {'form': form, 'es_edicion': True})

def eliminar_empresa(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk)
    if request.method == 'POST':
        empresa.delete()
        return redirect('lista_empresas')
    return render(request, 'inventario/confirmar_eliminar.html', {'objeto': empresa, 'tipo': 'Empresa'})


# --- VISTAS DE PRODUCTO ---
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'inventario/lista_productos.html', {'productos': productos})

def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'inventario/crear_producto.html', {'form': form})

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

def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('lista_productos')
    return render(request, 'inventario/confirmar_eliminar.html', {'objeto': producto, 'tipo': 'Producto'})