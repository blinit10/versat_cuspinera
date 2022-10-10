# Generated by Django 4.0.4 on 2022-09-20 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('nombre', models.CharField(max_length=255)),
                ('nombre_ingles', models.CharField(max_length=255)),
                ('precio', models.FloatField()),
                ('precio_lb', models.FloatField(blank=True, null=True, verbose_name='Precio por libra')),
                ('um', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Unidad de medida')),
                ('proveedor', models.CharField(max_length=255)),
                ('marca', models.CharField(max_length=255)),
                ('subcategoria', models.CharField(max_length=255)),
                ('descripcion', models.TextField(verbose_name='Descripción')),
                ('descripcion_ingles', models.TextField(verbose_name='Descripción Traducida')),
                ('municipios', models.CharField(max_length=500)),
                ('cantidad_inventario', models.IntegerField()),
                ('tags', models.CharField(max_length=500)),
                ('visible', models.BooleanField(default=False)),
                ('ventas', models.IntegerField(default=0)),
                ('sku', models.CharField(help_text='Código interno de la empresa', max_length=255, primary_key=True, serialize=False)),
                ('upc', models.CharField(blank=True, help_text='Concepto global de un producto. Opcional', max_length=255, null=True)),
                ('cantidad_maxima', models.IntegerField(default=2, verbose_name='Cantidad máxima')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': '01 - Producto',
            },
        ),
    ]
