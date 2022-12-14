# Generated by Django 4.0.4 on 2022-10-24 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion', '0007_rename_llave_datosorganizacion_key_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='datosorganizacion',
            old_name='organismmo',
            new_name='organismo',
        ),
        migrations.AddField(
            model_name='datosorganizacion',
            name='bill_format',
            field=models.CharField(default='SPMC', max_length=255, verbose_name='Formato para nombrar facturas'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='datosorganizacion',
            name='bill_number',
            field=models.IntegerField(default=0, verbose_name='Número de factura'),
        ),
    ]
