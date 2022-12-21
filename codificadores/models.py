from django.db import models

# Create your models here.

class Cargo(models.Model):
    cargo = models.CharField(max_length=255)

    def __str__(self):
        return '{}'.format(self.cargo)

    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = '01 - Cargos'


class Comercial(models.Model):
    nombres_apellidos = models.CharField(max_length=255, verbose_name='Nombres y Apellidos')
    ci = models.CharField(max_length=255, verbose_name='Carnet de Identidad', unique=True, primary_key=True)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, related_name='comerciales_cargo')

    def __str__(self):
        return '{}'.format(self.nombres_apellidos)

    class Meta:
        verbose_name = 'Comercial'
        verbose_name_plural = '02 - Comerciales'

class PersonalAutorizado(models.Model):
    entidad = models.ForeignKey('configuracion.Entidad', on_delete=models.CASCADE, related_name='autorizados_entidad')
    nombres_apellidos = models.CharField(max_length=255, verbose_name='Nombres y Apellidos')
    ci = models.CharField(max_length=255, verbose_name='Carnet de Identidad')
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, related_name='autorizados_cargo')

    def __str__(self):
        return '{}'.format(self.nombres_apellidos)

    class Meta:
        verbose_name = 'Personal Autorizado'
        verbose_name_plural = '03 - Personal Autorizado'

class FormaPago(models.Model):
    TIPO_CHOICES = (
        ('cheque','Cheque'),
        ('efectivo','Efectivo'),
        ('gratis','Gratis'),
        ('otras','Otras Formas de Pago'),
    )
    forma = models.CharField(max_length=255, verbose_name='Forma de Pago')
    tipo = models.CharField(max_length=255, choices=TIPO_CHOICES, verbose_name='Tipo de Pago')

    def __str__(self):
        return '{}'.format(self.forma)

    class Meta:
        verbose_name = 'Forma de Pago'
        verbose_name_plural = '04 - Formas de Pago'

class Operacion(models.Model):
    descripcion = models.CharField(max_length=255, verbose_name='Descripción')

    def __str__(self):
        return '{}'.format(self.descripcion)

    class Meta:
        verbose_name = 'Operación'
        verbose_name_plural = '05 - Operaciones'


class CuentaBancaria(models.Model):
    cuenta = models.CharField(max_length=500)
    codigo_intercambio = models.CharField(max_length=500, verbose_name='Código de Intercambio')
    nombre = models.CharField(max_length=255)
    moneda = models.ForeignKey('configuracion.Moneda', on_delete=models.CASCADE, related_name='cuentas_bancarias_moneda')
    sucursal = models.ForeignKey('configuracion.Sucursal', on_delete=models.CASCADE, related_name='cuentas_bancarias_sucursal')


    def __str__(self):
        return '{} - {}'.format(self.cuenta, self.nombre)

    class Meta:
        verbose_name = 'Cuenta Bancaria'
        verbose_name_plural = '06 - Cuentas Bancarias'


class TipoTalon(models.Model):
    CATEGORIA_CHOICES = (
        ('factura', 'Factura'),
        ('folio', 'Folio Preimpreso'),
    )
    codigo = models.CharField(max_length=255, unique=True, verbose_name='Código', primary_key=True)
    descripcion = models.CharField(max_length=255, verbose_name='Descripción')
    categoria = models.CharField(max_length=255, choices=CATEGORIA_CHOICES)

    def __str__(self):
        return '{}'.format(self.descripcion)

    class Meta:
        verbose_name = 'Tipo de Talón'
        verbose_name_plural = '07 - Tipos de Talón'
