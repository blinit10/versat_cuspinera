# Generated by Django 4.0.4 on 2022-12-10 17:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion', '0010_datosorganizacion_ruta_stream'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datosorganizacion',
            name='ruta_stream',
        ),
    ]
