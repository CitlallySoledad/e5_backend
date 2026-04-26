from django.db import transaction
from django.shortcuts import get_object_or_404

from productos.models import VarianteProducto
from usuarios.models import Usuario

from .exceptions import DomainError, InsufficientStockError
from .models import DetalleVenta, Venta


class VentaService:
    @staticmethod
    @transaction.atomic
    def registrar_venta(usuario_id, variante_id, cantidad, metodo_pago):
        usuario = get_object_or_404(Usuario, id_usuario=usuario_id)
        variante = get_object_or_404(VarianteProducto, id_variante=variante_id)

        if not usuario.activo:
            raise DomainError('El usuario no esta activo.')
        if cantidad <= 0:
            raise DomainError('La cantidad debe ser mayor que cero.')
        if not metodo_pago.strip():
            raise DomainError('El metodo de pago es obligatorio.')
        if variante.stock_actual < cantidad:
            raise InsufficientStockError('No hay suficiente stock.')

        total_venta = variante.precio_venta * cantidad
        venta = Venta.objects.create(
            usuario=usuario,
            total=total_venta,
            metodo_pago=metodo_pago.strip(),
        )

        DetalleVenta.objects.create(
            venta=venta,
            variante=variante,
            cantidad=cantidad,
            precio_unitario_aplicado=variante.precio_venta,
            subtotal=total_venta,
        )

        variante.stock_actual -= cantidad
        variante.save(update_fields=['stock_actual'])
        return venta
