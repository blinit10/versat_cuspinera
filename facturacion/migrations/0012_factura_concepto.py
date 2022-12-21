# Generated by Django 4.0.4 on 2022-10-24 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0011_factura_backup_bill'),
    ]

    operations = [
        migrations.AddField(
            model_name='factura',
            name='concepto',
            field=models.CharField(choices=[('001', 'Entidades'), ('002', 'Otras Formas de GE'), ('003', 'Personas Naturales'), ('004', 'Fuera del País')], default='004', max_length=255),
        ),
    ]
