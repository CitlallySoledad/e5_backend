import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0001_initial'),
        ('usuarios', '0001_initial'),
        ('ventas', '0003_alter_categoria_nombre_alter_detalleventa_venta'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL('DROP TABLE IF EXISTS ventas_detalleventa'),
                migrations.RunSQL('DROP TABLE IF EXISTS ventas_varianteproducto'),
                migrations.RunSQL('DROP TABLE IF EXISTS ventas_producto'),
                migrations.RunSQL('DROP TABLE IF EXISTS ventas_categoria'),
                migrations.RunSQL('DROP TABLE IF EXISTS ventas_venta'),
            ],
            state_operations=[
                migrations.DeleteModel(name='DetalleVenta'),
                migrations.DeleteModel(name='Venta'),
                migrations.DeleteModel(name='Categoria'),
                migrations.DeleteModel(name='Producto'),
                migrations.DeleteModel(name='VarianteProducto'),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id_venta', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_venta', models.DateTimeField(auto_now_add=True)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('metodo_pago', models.CharField(max_length=50)),
                ('usuario', models.ForeignKey(blank=True, db_column='id_usuario', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ventas', to='usuarios.usuario')),
            ],
            options={
                'db_table': 'ventas',
                'ordering': ['-fecha_venta'],
            },
        ),
        migrations.CreateModel(
            name='DetalleVenta',
            fields=[
                ('id_detalle', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField()),
                ('precio_unitario_aplicado', models.DecimalField(decimal_places=2, max_digits=10)),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('variante', models.ForeignKey(db_column='id_variante', on_delete=django.db.models.deletion.PROTECT, related_name='detalles_venta', to='productos.varianteproducto')),
                ('venta', models.ForeignKey(db_column='id_venta', on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='ventas.venta')),
            ],
            options={
                'db_table': 'detalle_ventas',
            },
        ),
    ]
