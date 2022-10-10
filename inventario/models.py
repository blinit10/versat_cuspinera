from django.db import models


# Create your models here.
class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    precio = models.FloatField()
    precio_lb = models.FloatField(null=True, blank=True, verbose_name='Precio por libra')
    um = models.CharField(max_length=255, default='', null=True, blank=True, verbose_name='Unidad de medida')
    proveedor = models.CharField(max_length=255)
    marca = models.CharField(max_length=255)
    subcategoria = models.CharField(max_length=255)
    descripcion = models.TextField(verbose_name='Descripción')
    municipios = models.CharField(max_length=500)
    cantidad_inventario = models.IntegerField()
    visible = models.BooleanField(default=False)
    sku = models.CharField(max_length=255, help_text='Código interno de la empresa', primary_key=True)
    upc = models.CharField(max_length=255, null=True, blank=True, help_text='Concepto global de un producto. Opcional')
    cantidad_maxima = models.IntegerField(default=2, verbose_name='Cantidad máxima')

    def __str__(self):
        return '{} - {}'.format(self.sku, self.nombre)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = '01 - Productos'
