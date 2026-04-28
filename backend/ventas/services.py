from django.db import transaction
from django.shortcuts import get_object_or_404

from .exceptions import DomainError, InsufficientStockError
from .models import Categoria, DetalleVenta, Producto, VarianteProducto, Venta


class InventarioService:
    @staticmethod
    def crear_categoria(nombre):
        nombre_normalizado = nombre.strip()
        if not nombre_normalizado:
            raise DomainError('El nombre de la categoria es obligatorio.')
        if Categoria.objects.filter(nombre__iexact=nombre_normalizado).exists():
            raise DomainError('La categoria ya existe.')
        return Categoria.objects.create(nombre=nombre_normalizado)

    @staticmethod
    def crear_producto_con_categoria(*, nombre, marca, categoria_id, descripcion=''):
        nombre_normalizado = nombre.strip()
        marca_normalizada = marca.strip()
        if not nombre_normalizado:
            raise DomainError('El nombre del producto es obligatorio.')
        if not marca_normalizada:
            raise DomainError('La marca es obligatoria.')
        categoria = get_object_or_404(Categoria, id=categoria_id)
        return Producto.objects.create(
            nombre=nombre_normalizado,
            marca=marca_normalizada,
            categoria=categoria,
            descripcion=descripcion.strip(),
        )

    @staticmethod
    def crear_variante(*, producto_id, talla, color, sku, precio_venta, stock_actual):
        producto = get_object_or_404(Producto, id=producto_id)
        if stock_actual < 0:
            raise DomainError('El stock no puede ser negativo.')
        if precio_venta <= 0:
            raise DomainError('El precio de venta debe ser mayor que cero.')
        if VarianteProducto.objects.filter(sku__iexact=sku.strip()).exists():
            raise DomainError('El SKU ya existe.')
        return VarianteProducto.objects.create(
            producto=producto,
            talla=talla.strip(),
            color=color.strip(),
            sku=sku.strip(),
            precio_venta=precio_venta,
            stock_actual=stock_actual,
        )


class VentaService:
    @staticmethod
    @transaction.atomic
    def registrar_venta(variante_id, cantidad, metodo_pago):
        variante = get_object_or_404(VarianteProducto, id=variante_id)
        if cantidad <= 0:
            raise DomainError('La cantidad debe ser mayor que cero.')
        if not metodo_pago.strip():
            raise DomainError('El metodo de pago es obligatorio.')
        if variante.stock_actual < cantidad:
            raise InsufficientStockError('No hay suficiente stock.')

        total_venta = variante.precio_venta * cantidad
        nueva_venta = Venta.objects.create(total=total_venta, metodo_pago=metodo_pago.strip())

        DetalleVenta.objects.create(
            venta=nueva_venta,
            variante=variante,
            cantidad=cantidad,
            precio_unitario_aplicado=variante.precio_venta,
            subtotal=total_venta,
        )
        variante.stock_actual -= cantidad
        variante.save(update_fields=['stock_actual'])
        return nueva_venta
