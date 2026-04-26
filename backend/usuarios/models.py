from django.db import models


class Role(models.Model):
    id_role = models.AutoField(primary_key=True)
    nombre_role = models.CharField(max_length=80, unique=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        db_table = 'roles'
        ordering = ['nombre_role']

    def __str__(self):
        return self.nombre_role


class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    password_hash = models.CharField(max_length=255)
    nombre_completo = models.CharField(max_length=180)
    role = models.ForeignKey(
        Role,
        on_delete=models.PROTECT,
        db_column='id_role',
        related_name='usuarios',
    )
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'usuarios'
        ordering = ['username']

    def __str__(self):
        return self.username
