from django.db import models


# Create your models here.
from django.utils.safestring import mark_safe


class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    precio = models.FloatField()
    precio_b2b = models.FloatField(default=0)
    precio_lb = models.FloatField(null=True, blank=True, verbose_name='Precio por libra')
    um = models.CharField(max_length=255, default='', null=True, blank=True, verbose_name='Unidad de medida')
    proveedor = models.CharField(max_length=255)
    marca = models.CharField(max_length=255)
    subcategoria = models.CharField(max_length=255)
    descripcion = models.TextField(verbose_name='Descripción')
    municipios = models.CharField(max_length=500)
    cantidad_inventario = models.IntegerField()
    imagen = models.CharField(max_length=800, null=True, blank=True)
    visible = models.BooleanField(default=False)
    sku = models.CharField(max_length=255, help_text='Código interno de la empresa', primary_key=True)
    upc = models.CharField(max_length=255, null=True, blank=True, help_text='Concepto global de un producto. Opcional')
    cantidad_maxima = models.IntegerField(default=2, verbose_name='Cantidad máxima')

    def __str__(self):
        return '{} - {}'.format(self.sku, self.nombre)

    def img(self):
        return mark_safe('<img src="https://www.diplomarket.com{}" width="150px" height="150px"></img>'.format(self.imagen))

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = '01 - Productos'
        ordering = ['subcategoria', 'marca', 'precio_b2b', 'precio','nombre', '-cantidad_inventario']
