import uuid as uuid
from datetime import datetime

from django.core.validators import MinValueValidator
from django.db import models


# Create your models here.


class Talon(models.Model):
    numero_serie = models.CharField(max_length=500, verbose_name='Número de Serie', primary_key=True)
    descripcion = models.CharField(max_length=500, verbose_name='Descripción')
    tipo = models.ForeignKey('codificadores.TipoTalon', on_delete=models.CASCADE, related_name='talones')
    tipo_factura = models.CharField(max_length=500, verbose_name='Bienes y Servicios')

    def __str__(self):
        return '{}'.format(self.descripcion)

    class Meta:
        verbose_name = 'Talón'
        verbose_name_plural = '01 - Talones'


class Factura(models.Model):
    # CONCEPTO_CHOICES = (
    #     ('001', 'Business to business'),
    #     ('002', 'Online'),
    #     ('003', 'Pago anticipado'),
    #     ('004', 'Pago en el exterior'),
    # )
    CONCEPTO_CHOICES = (
        ('001', 'Entidades'),
        ('002', 'Otras Formas de GE'),
        ('003', 'Personas Naturales'),
        ('004', 'Fuera del País'),
    )
    talon = models.ForeignKey(Talon, on_delete=models.CASCADE, related_name='facturas_talon')
    entidad = models.ForeignKey('configuracion.Entidad', on_delete=models.CASCADE, related_name='facturas_entidad')
    moneda = models.ForeignKey('configuracion.Moneda', on_delete=models.CASCADE, related_name='facturas_moneda')
    tasa = models.FloatField(default=24)
    almacen = models.ForeignKey('configuracion.Almacen', on_delete=models.CASCADE, related_name='orden_almacen',
                                default='0002')
    fecha = models.DateField(default=datetime.now)
    concepto = models.CharField(max_length=255, default='004', choices=CONCEPTO_CHOICES)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    comercial = models.ForeignKey('codificadores.Comercial', on_delete=models.CASCADE,
                                  related_name='facturas_comercial')
    cuenta = models.ForeignKey('codificadores.CuentaBancaria', on_delete=models.CASCADE,
                               related_name='facturas_cuenta_bancaria')
    forma = models.ForeignKey('codificadores.FormaPago', on_delete=models.CASCADE, related_name='facturas_forma_pago')
    operacion = models.ForeignKey('codificadores.Operacion', on_delete=models.CASCADE,
                                  related_name='facturas_operacion')
    aprobada = models.BooleanField(default=False)
    subtotal_servicios = models.FloatField(default=0)
    subtotal_productos = models.FloatField(default=0)
    total = models.FloatField(default=0)
    backup_bill = models.CharField(max_length=500, null=True, blank=True, editable=False)
    faltantes = models.TextField(
        default="------------------------------------------------------------------------------"
                "------------------------------------------------------------------------")
    nota = models.TextField(default="", null=True, blank=True)
    exportada_como = models.CharField(max_length=500, null=True, blank=True, editable=False)

    def __str__(self):
        return '{}'.format(self.uuid)

    def save(self, *args, **kwargs):

        super(Factura, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = '02 - Facturas'
        ordering = ['-fecha']


class ComponenteProductoFactura(models.Model):
    CONCEPTO_CHOICES = (
        ('001', 'B to B'),
        ('002', 'VENTA ONLINE'),
        ('003', 'VENTA DIRECTA'),
    )
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name='productos_factura', null=True,
                                blank=True)
    almacen = models.ForeignKey('configuracion.Almacen', on_delete=models.CASCADE, related_name='componentes_almacen')
    producto = models.ForeignKey('inventario.Producto', on_delete=models.PROTECT, related_name='componentes_producto')
    concepto = models.CharField(max_length=255, choices=CONCEPTO_CHOICES, null=True, blank=True)
    cantidad = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    recargo = models.FloatField(default=0)
    descuento = models.FloatField(default=0)
    precio = models.FloatField(null=True, blank=True, verbose_name='Precio')
    importe = models.FloatField(default=0, verbose_name='Importe')
    settled_import = models.FloatField(default=0)

    def __str__(self):

        return '{}'.format(self.producto.nombre)

    def save(self, *args, **kwargs):
        self.almacen = self.factura.almacen
        for item in self.CONCEPTO_CHOICES:
            if item[1] == self.factura.operacion.descripcion:
                self.concepto = item[0]
        self.factura.total = self.factura.total - self.settled_import
        self.factura.subtotal_productos = self.factura.subtotal_productos - self.settled_import
        subtotal = (self.precio + (self.precio * self.recargo / 100) - self.descuento) * self.cantidad
        self.factura.total = self.factura.total + subtotal
        self.factura.subtotal_productos = self.factura.subtotal_productos + subtotal
        self.importe = subtotal
        self.settled_import = subtotal
        super(ComponenteProductoFactura, self).save(*args, **kwargs)
        self.factura.save()
        super(ComponenteProductoFactura, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'


class ComponenteServicioFactura(models.Model):
    CONCEPTO_CHOICES = (
        ('001', 'Servicio de transportación'),
    )
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name='servicios_factura', null=True,
                                blank=True)
    servicio = models.ForeignKey('precios.Servicio', on_delete=models.CASCADE, related_name='componentes_servicio')
    concepto = models.CharField(max_length=255, choices=CONCEPTO_CHOICES)
    cantidad = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    recargo = models.FloatField(default=0)
    descuento = models.FloatField(default=0)
    importe = models.FloatField(default=0)
    settled_import = models.FloatField(default=0)

    def __str__(self):
        return '{}'.format(self.servicio.descripcion)

    def save(self, *args, **kwargs):
        self.factura.total = self.factura.total - self.settled_import
        self.factura.subtotal_servicios = self.factura.subtotal_servicios - self.settled_import
        subtotal = (self.importe + (self.importe * self.recargo / 100) - self.descuento) * self.cantidad
        self.factura.total = self.factura.total + subtotal
        self.factura.subtotal_servicios = self.factura.subtotal_servicios + subtotal
        self.settled_import = subtotal
        super(ComponenteServicioFactura, self).save(*args, **kwargs)
        self.factura.save()
        super(ComponenteServicioFactura, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
