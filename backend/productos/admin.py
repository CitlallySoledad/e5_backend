from django.contrib import admin

from .models import Categoria, Color, Marca, Producto, Talla, VarianteProducto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id_categoria', 'nombre')
    search_fields = ('nombre',)


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('id_marca', 'nombre')
    search_fields = ('nombre',)


@admin.register(Talla)
class TallaAdmin(admin.ModelAdmin):
    list_display = ('id_talla', 'nombre')
    search_fields = ('nombre',)


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('id_color', 'nombre', 'codigo_hex')
    search_fields = ('nombre', 'codigo_hex')


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id_producto', 'nombre', 'categoria', 'marca')
    list_filter = ('categoria', 'marca')
    search_fields = ('nombre', 'descripcion')


@admin.register(VarianteProducto)
class VarianteProductoAdmin(admin.ModelAdmin):
    list_display = ('id_variante', 'producto', 'talla', 'color', 'sku', 'codigo_barras', 'precio_venta', 'stock_actual')
    list_filter = ('talla', 'color')
    search_fields = ('sku', 'codigo_barras', 'producto__nombre')
