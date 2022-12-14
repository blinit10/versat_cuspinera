# Generated by Django 4.0.4 on 2022-12-11 17:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion', '0011_remove_datosorganizacion_ruta_stream'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProveedorPropio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('cfg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proveedores_cfg', to='configuracion.datosorganizacion')),
            ],
            options={
                'verbose_name': 'Proveedor propio de la empresa',
                'verbose_name_plural': 'Proveedores propios de la empresa',
            },
        ),
    ]
