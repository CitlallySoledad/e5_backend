from django.contrib import admin
from .models import Categoria, DetalleVenta, Producto, VarianteProducto, Venta

# Esto permite ver y editar las tablas desde el navegador
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(VarianteProducto)
admin.site.register(Venta)
admin.site.register(DetalleVenta)