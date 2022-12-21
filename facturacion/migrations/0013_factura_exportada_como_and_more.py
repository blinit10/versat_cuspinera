# Generated by Django 4.0.4 on 2022-10-24 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0012_factura_concepto'),
    ]

    operations = [
        migrations.AddField(
            model_name='factura',
            name='exportada_como',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='componenteproductofactura',
            name='importe',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='componenteproductofactura',
            name='precio',
            field=models.FloatField(default=0),
        ),
    ]