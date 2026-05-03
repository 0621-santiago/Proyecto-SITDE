from django.db import models

# CLIENTES
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre


# PROVEEDORES
class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    empresa = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre


# PRODUCTOS
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.FloatField()
    stock = models.IntegerField()
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


# VENTAS
class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.FloatField()

    def __str__(self):
        return f"Venta {self.id}"


# DETALLE DE VENTA (relación productos - ventas)
class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    subtotal = models.FloatField()
