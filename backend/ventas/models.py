from django.db import models

from productos.models import VarianteProducto
from usuarios.models import Usuario


class Venta(models.Model):
    id_venta = models.AutoField(primary_key=True)
    fecha_venta = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    metodo_pago = models.CharField(max_length=50)
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        db_column='id_usuario',
        related_name='ventas',
    )

    class Meta:
        db_table = 'ventas'
        ordering = ['-fecha_venta']

    def __str__(self):
        return f"Venta #{self.id_venta}"


class DetalleVenta(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    venta = models.ForeignKey(
        Venta,
        on_delete=models.CASCADE,
        db_column='id_venta',
        related_name='detalles',
    )
    variante = models.ForeignKey(
        VarianteProducto,
        on_delete=models.PROTECT,
        db_column='id_variante',
        related_name='detalles_venta',
    )
    cantidad = models.IntegerField()
    precio_unitario_aplicado = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'detalle_ventas'

    def __str__(self):
        return f"Detalle #{self.id_detalle}"
