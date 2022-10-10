from django.db import models


# Create your models here.
class Servicio(models.Model):
    codigo = models.CharField(max_length=255, verbose_name='Código', primary_key=True)
    descripcion = models.CharField(max_length=255, verbose_name='Descripción')
    um = models.CharField(max_length=255, verbose_name='Unidad de medida')

    def __str__(self):
        return '{}'.format(self.descripcion)

    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = '01 - Servicios'
