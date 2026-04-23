# productos/models.py
from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre


class Marca(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Talla(models.Model):
    nombre = models.CharField(max_length=10)  # XS, S, M, L, XL, 28, 30...

    def __str__(self):
        return self.nombre


class Color(models.Model):
    nombre = models.CharField(max_length=50)
    codigo_hex = models.CharField(max_length=7, blank=True)  # #FFFFFF

    def __str__(self):
        return self.nombre


class Producto(models.Model):

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    marca = models.ForeignKey(Marca, on_delete=models.SET_NULL, null=True)
    # Atributos del producto
    tallas = models.ManyToManyField(Talla, blank=True)
    colores = models.ManyToManyField(Color, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class VarianteProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE,
                                  related_name='variantes')
    talla = models.ForeignKey(Talla, on_delete=models.SET_NULL, null=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True)
    sku = models.CharField(max_length=100, unique=True)
    codigo_barras = models.CharField(max_length=100, blank=True)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    stock_actual = models.IntegerField(default=0)

    class Meta:
        unique_together = ('producto', 'talla', 'color')

    def __str__(self):
        return f"{self.producto} - {self.talla} - {self.color}"
