from django.core.validators import MinValueValidator
from django.db import models


# Create your models here.
from django.utils.safestring import mark_safe
class DatosOrganizacion(models.Model):
    codigo = models.CharField(max_length=255, verbose_name='Código')
    nombre = models.CharField(max_length=255)
    organismo = models.CharField(max_length=255)
    telefono = models.CharField(max_length=255, null=True, blank=True, verbose_name='Teléfono', help_text='Opcional')
    direccion = models.TextField(verbose_name='Dirección')
    logotipo = models.ImageField(upload_to='imagenes/')
    presidente = models.CharField(max_length=255)
    contador = models.CharField(max_length=255)
    nit = models.CharField(max_length=255)
    ircc = models.CharField(max_length=255)
    #cfg for connecting with the diplomarket api
    key = models.CharField(max_length=800)
    server = models.CharField(max_length=800)
    test = models.BooleanField(verbose_name='Entorno de prueba')
    bill_format = models.CharField(max_length=255, verbose_name='Formato para nombrar facturas')
    bill_number = models.IntegerField(default=0, verbose_name='Número de factura')
    bills_dir = models.CharField(max_length=500, verbose_name='Dirección para guardar las facturas')

    def __str__(self):
        return '{}'.format(self.nombre)

    def miniatura(self):
        return mark_safe('<img src="' + self.logotipo.url + '" width="120">')

    miniatura.short_description = 'Vista previa'
    miniatura.allow_tags = True

    class Meta:
        verbose_name = 'Datos de la Organización'
        verbose_name_plural = '00 - Datos de la Organización'


class Unidad(models.Model):
    codigo = models.CharField(max_length=255, unique=True, verbose_name='Código', primary_key=True)
    nombre = models.CharField(max_length=255)
    direccion = models.TextField(verbose_name='Dirección')
    correo = models.EmailField()
    reeup = models.CharField(max_length=255, null=True, blank=True, unique=True, help_text='Opcional')

    def __str__(self):
        return '{} - {}'.format(self.codigo, self.nombre)

    class Meta:
        verbose_name = 'Unidad'
        verbose_name_plural = '01 - Unidades'


class Area(models.Model):
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE, related_name='areas_unidad')
    clave = models.CharField(default='001', unique=True, max_length=3, primary_key=True)
    descripcion = models.CharField(max_length=255, verbose_name='Descripción')
    direccion = models.TextField(verbose_name='Dirección')

    def __str__(self):
        return '{} - {}'.format(self.clave, self.descripcion)

    class Meta:
        verbose_name = 'Área'
        verbose_name_plural = '02 - Áreas'


class Trabajador(models.Model):
    codigo = models.CharField(max_length=255, verbose_name='Código', unique=True, primary_key=True)
    nombres = models.CharField(max_length=255)
    primer_apellido = models.CharField(max_length=255)
    segundo_apellido = models.CharField(max_length=255)
    nro_indentidad = models.CharField(max_length=255, verbose_name='Nro. Identidad', unique=True)
    direccion = models.TextField(verbose_name='Dirección')
    correo = models.EmailField()

    def __str__(self):
        return '{} {} {}'.format(self.nombres, self.primer_apellido, self.segundo_apellido)

    class Meta:
        verbose_name = 'Trabajador'
        verbose_name_plural = '03 - Trabajadores'


class Almacen(models.Model):
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE, related_name='almacenes_unidad')
    codigo = models.CharField(max_length=255, verbose_name='Código', unique=True, primary_key=True)
    nombre = models.CharField(max_length=255)
    jefe_almacen = models.ForeignKey(Trabajador, on_delete=models.CASCADE, related_name='almacenes_jefe_almacen',
                                     verbose_name='Jefe de Almacén')
    direccion = models.TextField(verbose_name='Dirección')

    def __str__(self):
        return '{}'.format(self.nombre)

    class Meta:
        verbose_name = 'Almacén'
        verbose_name_plural = '04 - Almacenes'


class Custodio(models.Model):
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE, related_name='custodios_unidad')
    codigo = models.CharField(max_length=255, verbose_name='Código', unique=True, primary_key=True)
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return '{}'.format(self.nombre)

    class Meta:
        verbose_name = 'Custodio'
        verbose_name_plural = '05 - Custodios'


class Entidad(models.Model):
    codigo = models.CharField(max_length=255, verbose_name='Código', unique=True, primary_key=True)
    nombre = models.CharField(max_length=255)
    reeup = models.CharField(max_length=255, unique=True)
    abreviatura = models.CharField(null=True, blank=True, max_length=255, help_text='Opcional')
    direccion = models.TextField(verbose_name='Dirección', blank=True, null=True, help_text='Opcional')
    correo = models.EmailField(null=True, blank=True, help_text='Opcional')
    telefono = models.CharField(max_length=255, null=True, blank=True, verbose_name='Teléfono', help_text='Opcional')
    nit = models.CharField(max_length=255, null=True, blank=True, help_text='Opcional')
    ircc = models.CharField(max_length=255, null=True, blank=True, help_text='Opcional')
    provincia = models.CharField(max_length=255, null=True, blank=True, help_text='Opcional')
    pais = models.CharField(max_length=255, null=True, blank=True, help_text='Opcional')

    def __str__(self):
        return '{}'.format(self.nombre)

    class Meta:
        verbose_name = 'Entidad/Persona Natural'
        verbose_name_plural = '06 - Entidades/Personas Naturales'


class Banco(models.Model):
    codigo = models.CharField(max_length=255, verbose_name='Código', unique=True, primary_key=True)
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return '{}'.format(self.nombre)

    class Meta:
        verbose_name = 'Banco'
        verbose_name_plural = '07 - Bancos'


class Sucursal(models.Model):
    numero = models.PositiveIntegerField(primary_key=True, default=1, verbose_name='Número',
                                         validators=[MinValueValidator(1)])
    direccion = models.TextField(verbose_name='Dirección')

    def __str__(self):
        return '{}, {}'.format(str(self.numero), self.direccion)

    class Meta:
        verbose_name = 'Sucursal'
        verbose_name_plural = '08 - Sucursales'


class Ejercicio(models.Model):  # años fiscales
    nombre = models.CharField(max_length=255)
    inicio = models.DateField()
    fin = models.DateField()

    def __str__(self):
        return '{}'.format(self.nombre)

    class Meta:
        verbose_name = 'Ejercicio'
        verbose_name_plural = '09 - Ejercicios'


class Periodo(models.Model):  # meses dentro del año
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)
    inicio = models.DateField()
    fin = models.DateField()

    def __str__(self):
        return '{}'.format(self.nombre)

    class Meta:
        verbose_name = 'Período'
        verbose_name_plural = 'Períodos'


class Moneda(models.Model):
    TIPO_CHOICES = (
        ('contable', 'Moneda Contable'),
        ('otras', 'Otras Monedas')
    )
    tipo = models.CharField(max_length=255, choices=TIPO_CHOICES)
    nombre = models.CharField(max_length=255)
    siglas = models.CharField(max_length=255)
    tasa = models.FloatField(default=1, help_text='Establecer en 1 si se está insertando una moneda contable')

    def __str__(self):
        return '{}'.format(self.nombre)

    class Meta:
        verbose_name = 'Moneda'
        verbose_name_plural = '10 - Monedas'


class ConceptoVenta(models.Model):
    codigo = models.CharField(max_length=255, verbose_name='Código', unique=True)
    descripcion = models.CharField(max_length=255, verbose_name='Descripción')
    concepto = models.CharField(max_length=255, verbose_name='Concepto Obligación')
    en_experimento = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.descripcion)

    class Meta:
        verbose_name = 'Concepto de venta'
        verbose_name_plural = '11 - Conceptos de venta'
