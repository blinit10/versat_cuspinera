# Generated by Django 4.0.4 on 2022-09-26 00:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0004_factura_aprobada_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='componenteserviciofactura',
            name='precio',
        ),
        migrations.AlterField(
            model_name='componenteproductofactura',
            name='importe',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='componenteproductofactura',
            name='precio',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='componenteserviciofactura',
            name='descuento',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='componenteserviciofactura',
            name='importe',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='componenteserviciofactura',
            name='recargo',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='factura',
            name='fecha',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='factura',
            name='tasa',
            field=models.FloatField(default=24),
        ),
    ]
