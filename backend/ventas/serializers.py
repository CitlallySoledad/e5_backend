from rest_framework import serializers
from .models import Categoria, DetalleVenta, Producto, VarianteProducto, Venta

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

    def validate_nombre(self, value):
        nombre = value.strip()
        if not nombre:
            raise serializers.ValidationError('El nombre es obligatorio.')
        return nombre


class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.ReadOnlyField(source='categoria.nombre')

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'marca', 'descripcion', 'categoria', 'categoria_nombre']

    def validate_nombre(self, value):
        nombre = value.strip()
        if not nombre:
            raise serializers.ValidationError('El nombre es obligatorio.')
        return nombre

    def validate_marca(self, value):
        marca = value.strip()
        if not marca:
            raise serializers.ValidationError('La marca es obligatoria.')
        return marca


class VarianteSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.ReadOnlyField(source='producto.nombre')

    class Meta:
        model = VarianteProducto
        fields = ['id', 'producto', 'producto_nombre', 'talla', 'color', 'sku', 'precio_venta', 'stock_actual']

    def validate_sku(self, value):
        sku = value.strip()
        if not sku:
            raise serializers.ValidationError('El SKU es obligatorio.')
        return sku

    def validate_precio_venta(self, value):
        if value <= 0:
            raise serializers.ValidationError('El precio de venta debe ser mayor que cero.')
        return value

    def validate_stock_actual(self, value):
        if value < 0:
            raise serializers.ValidationError('El stock no puede ser negativo.')
        return value


class DetalleVentaSerializer(serializers.ModelSerializer):
    producto = serializers.ReadOnlyField(source='variante.producto.nombre')

    class Meta:
        model = DetalleVenta
        fields = ['id', 'variante', 'producto', 'cantidad', 'precio_unitario_aplicado', 'subtotal']


class VentaSerializer(serializers.ModelSerializer):
    detalles = DetalleVentaSerializer(many=True, read_only=True)

    class Meta:
        model = Venta
        fields = ['id', 'fecha_venta', 'total', 'metodo_pago', 'detalles']


class VentaCreateSerializer(serializers.Serializer):
    variante_id = serializers.IntegerField(min_value=1)
    cantidad = serializers.IntegerField(min_value=1)
    metodo_pago = serializers.CharField(max_length=50)

    def validate_metodo_pago(self, value):
        metodo_pago = value.strip()
        if not metodo_pago:
            raise serializers.ValidationError('El metodo de pago es obligatorio.')
        return metodo_pago
