import re

from rest_framework import serializers

from .models import Categoria, Color, Marca, Producto, Talla, VarianteProducto


class NombreUnicoMixin:
    def validate_nombre(self, value):
        nombre = value.strip()
        if not nombre:
            raise serializers.ValidationError('El nombre es obligatorio.')
        return nombre


class CategoriaSerializer(NombreUnicoMixin, serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id_categoria', 'nombre']


class MarcaSerializer(NombreUnicoMixin, serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = ['id_marca', 'nombre']


class TallaSerializer(NombreUnicoMixin, serializers.ModelSerializer):
    class Meta:
        model = Talla
        fields = ['id_talla', 'nombre']


class ColorSerializer(NombreUnicoMixin, serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id_color', 'nombre', 'codigo_hex']

    def validate_codigo_hex(self, value):
        codigo_hex = value.strip()
        if not codigo_hex:
            raise serializers.ValidationError('El codigo hexadecimal es obligatorio.')
        if not re.fullmatch(r'#[0-9A-Fa-f]{6}', codigo_hex):
            raise serializers.ValidationError('El codigo hexadecimal debe tener formato #RRGGBB.')
        return codigo_hex.upper()


class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.ReadOnlyField(source='categoria.nombre')
    marca_nombre = serializers.ReadOnlyField(source='marca.nombre')

    class Meta:
        model = Producto
        fields = [
            'id_producto',
            'nombre',
            'descripcion',
            'categoria',
            'categoria_nombre',
            'marca',
            'marca_nombre',
        ]

    def validate_nombre(self, value):
        nombre = value.strip()
        if not nombre:
            raise serializers.ValidationError('El nombre del producto es obligatorio.')
        return nombre

    def validate_descripcion(self, value):
        return value.strip() if value else ''


class VarianteProductoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.ReadOnlyField(source='producto.nombre')
    talla_nombre = serializers.ReadOnlyField(source='talla.nombre')
    color_nombre = serializers.ReadOnlyField(source='color.nombre')
    color_hex = serializers.ReadOnlyField(source='color.codigo_hex')

    class Meta:
        model = VarianteProducto
        fields = [
            'id_variante',
            'producto',
            'producto_nombre',
            'talla',
            'talla_nombre',
            'color',
            'color_nombre',
            'color_hex',
            'sku',
            'codigo_barras',
            'precio_venta',
            'stock_actual',
        ]

    def validate_sku(self, value):
        sku = value.strip().upper()
        if not sku:
            raise serializers.ValidationError('El SKU es obligatorio.')
        return sku

    def validate_codigo_barras(self, value):
        codigo_barras = value.strip()
        if not codigo_barras:
            raise serializers.ValidationError('El codigo de barras es obligatorio.')
        return codigo_barras

    def validate_precio_venta(self, value):
        if value <= 0:
            raise serializers.ValidationError('El precio de venta debe ser mayor que cero.')
        return value

    def validate_stock_actual(self, value):
        if value < 0:
            raise serializers.ValidationError('El stock no puede ser negativo.')
        return value
