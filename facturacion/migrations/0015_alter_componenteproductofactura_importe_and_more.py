# Generated by Django 4.0.4 on 2022-10-26 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0014_alter_factura_exportada_como'),
    ]

    operations = [
        migrations.AlterField(
            model_name='componenteproductofactura',
            name='importe',
            field=models.FloatField(default=0, verbose_name='Importe'),
        ),
        migrations.AlterField(
            model_name='componenteproductofactura',
            name='precio',
            field=models.FloatField(blank=True, null=True, verbose_name='Precio'),
        ),
    ]
