# Generated by Django 4.0.4 on 2022-12-09 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0004_remove_producto_ventas'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='imagen',
            field=models.CharField(blank=True, max_length=800, null=True),
        ),
    ]