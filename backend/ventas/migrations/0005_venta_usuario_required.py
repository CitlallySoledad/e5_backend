import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
        ('ventas', '0004_pdf_schema'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venta',
            name='usuario',
            field=models.ForeignKey(db_column='id_usuario', on_delete=django.db.models.deletion.PROTECT, related_name='ventas', to='usuarios.usuario'),
        ),
    ]
