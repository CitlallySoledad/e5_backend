from django.contrib import admin

from .models import Role, Usuario


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id_role', 'nombre_role')
    search_fields = ('nombre_role', 'descripcion')


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id_usuario', 'username', 'nombre_completo', 'role', 'activo')
    list_filter = ('role', 'activo')
    search_fields = ('username', 'nombre_completo')
