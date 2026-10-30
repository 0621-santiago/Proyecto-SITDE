from django.db import models
from django.contrib.auth.models import User

#  EMPRESA
class Empresa(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='empresa')
    nombre = models.CharField(max_length=150)
    nit = models.CharField(max_length=20, unique=True)
    municipio = models.CharField(max_length=100)
    telefono = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.nombre} ({self.nit})"

#  CLIENTES
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

#  PROVEEDORES
class Proveedor(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE) 
    nit = models.CharField(max_length=20)
    nombre = models.CharField(max_length=150)
    municipio = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)

    class Meta:
        unique_together = ('empresa', 'nit') 

    def __str__(self):
        return self.nombre

#  RECEPCIÓN DE MATERIA PRIMA
class RecepcionMP(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    fecha = models.DateField()
    litros = models.DecimalField(max_digits=10, decimal_places=2)
    densidad = models.DecimalField(max_digits=5, decimal_places=2)
    grasa_pct = models.DecimalField(max_digits=5, decimal_places=2)
    temperatura = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Recepción {self.fecha} - {self.litros}L"

#  PRODUCTOS
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

#  VENTAS
class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Venta {self.id}"

#  DETALLE DE VENTA
class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle de {self.producto.nombre} - Cantidad: {self.cantidad}"