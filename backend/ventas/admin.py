from django.contrib import admin
from .models import DetalleVenta, Venta


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('id_venta', 'fecha_venta', 'usuario', 'total', 'metodo_pago')
    list_filter = ('metodo_pago', 'fecha_venta')
    search_fields = ('usuario__username', 'usuario__nombre_completo')


@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ('id_detalle', 'venta', 'variante', 'cantidad', 'precio_unitario_aplicado', 'subtotal')
    search_fields = ('variante__sku', 'variante__producto__nombre')
