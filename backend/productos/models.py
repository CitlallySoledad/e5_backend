from django.db import models


class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'categorias'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Marca(models.Model):
    id_marca = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'marcas'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Talla(models.Model):
    id_talla = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'tallas'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Color(models.Model):
    id_color = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=80, unique=True)
    codigo_hex = models.CharField(max_length=7)

    class Meta:
        db_table = 'colores'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        db_column='id_categoria',
        related_name='productos',
    )
    marca = models.ForeignKey(
        Marca,
        on_delete=models.PROTECT,
        db_column='id_marca',
        related_name='productos',
    )

    class Meta:
        db_table = 'productos'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class VarianteProducto(models.Model):
    id_variante = models.AutoField(primary_key=True)
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        db_column='id_producto',
        related_name='variantes',
    )
    talla = models.ForeignKey(
        Talla,
        on_delete=models.PROTECT,
        db_column='id_talla',
        related_name='variantes',
    )
    color = models.ForeignKey(
        Color,
        on_delete=models.PROTECT,
        db_column='id_color',
        related_name='variantes',
    )
    sku = models.CharField(max_length=100, unique=True)
    codigo_barras = models.CharField(max_length=100, unique=True)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    stock_actual = models.IntegerField(default=0)

    class Meta:
        db_table = 'variantes_producto'
        ordering = ['producto__nombre', 'sku']

    def __str__(self):
        return self.sku
