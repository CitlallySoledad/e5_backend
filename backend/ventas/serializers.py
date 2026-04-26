from rest_framework import serializers

from .models import DetalleVenta, Venta


class DetalleVentaSerializer(serializers.ModelSerializer):
    producto = serializers.ReadOnlyField(source='variante.producto.nombre')
    sku = serializers.ReadOnlyField(source='variante.sku')

    class Meta:
        model = DetalleVenta
        fields = [
            'id_detalle',
            'variante',
            'producto',
            'sku',
            'cantidad',
            'precio_unitario_aplicado',
            'subtotal',
        ]


class VentaSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.ReadOnlyField(source='usuario.nombre_completo')
    detalles = DetalleVentaSerializer(many=True, read_only=True)

    class Meta:
        model = Venta
        fields = [
            'id_venta',
            'fecha_venta',
            'total',
            'metodo_pago',
            'usuario',
            'usuario_nombre',
            'detalles',
        ]


class VentaCreateSerializer(serializers.Serializer):
    usuario_id = serializers.IntegerField(min_value=1)
    variante_id = serializers.IntegerField(min_value=1)
    cantidad = serializers.IntegerField(min_value=1)
    metodo_pago = serializers.CharField(max_length=50)

    def validate_metodo_pago(self, value):
        metodo_pago = value.strip()
        if not metodo_pago:
            raise serializers.ValidationError('El metodo de pago es obligatorio.')
        return metodo_pago
