# Generated by Django 4.0.4 on 2022-09-23 16:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='producto',
            options={'verbose_name': 'Producto', 'verbose_name_plural': '01 - Productos'},
        ),
        migrations.RemoveField(
            model_name='producto',
            name='tags',
        ),
    ]
