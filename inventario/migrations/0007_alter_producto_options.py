# Generated by Django 4.0.5 on 2022-12-21 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0006_producto_precio_b2b'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='producto',
            options={'ordering': ['subcategoria', 'marca', 'precio_b2b', 'precio', 'nombre', '-cantidad_inventario'], 'verbose_name': 'Producto', 'verbose_name_plural': '01 - Productos'},
        ),
    ]