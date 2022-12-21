from django.contrib import admin

# InLines
from facturacion.actions import aprove, revert, export
from facturacion.models import Talon, ComponenteProductoFactura, ComponenteServicioFactura, Factura


class ComponenteProductoFacturaInLine(admin.StackedInline):
    model = ComponenteProductoFactura
    extra = 0
    min_num = 1
    readonly_fields = ['importe', ]
    autocomplete_fields = ['producto',]
    fieldsets = (
        ('Información Básica', {
            'fields': (
                'almacen', 'producto', ('concepto', 'cantidad'))}),
        ('Información Contable', {
            'fields': (
                ('recargo', 'descuento',), ('importe', 'precio'),)}),
    )


    def get_readonly_fields(self, request, obj=None):
        if obj and obj.aprobada is True:
            return ['almacen', 'producto', 'concepto', 'cantidad', 'recargo', 'descuento', 'precio', 'importe']
        return self.readonly_fields


class ComponenteServicioFacturaInLine(admin.StackedInline):
    model = ComponenteServicioFactura
    extra = 0
    fieldsets = (
        ('Información Básica', {
            'fields': (
                'servicio', ('concepto', 'cantidad'))}),
        ('Información Contable', {
            'fields': (
                ('recargo', 'descuento', 'importe'),)}),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.aprobada is True:
            return ['servicio', 'concepto', 'cantidad', 'recargo', 'descuento', 'importe']
        return self.readonly_fields


# fin InLines
# ModelAdmin
# fin de ModelAdmin
class FacturaAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'entidad', 'moneda', 'cuenta', 'forma', 'total', 'subtotal_productos', 'subtotal_servicios',
                    'aprobada', 'exportada_como']
    list_display_links = ['uuid', 'entidad', 'moneda', 'cuenta', 'forma', 'total', 'subtotal_productos',
                          'subtotal_servicios', 'aprobada']
    list_filter = ['talon', 'entidad', 'moneda', 'fecha', 'comercial', 'cuenta', 'forma', 'operacion', 'aprobada']
    readonly_fields = ['total', 'subtotal_productos', 'subtotal_servicios', 'aprobada', 'faltantes']
    inlines = [ComponenteProductoFacturaInLine, ComponenteServicioFacturaInLine]
    actions = [aprove, revert, export]

    def get_actions(self, request):
        actions = super(FacturaAdmin, self).get_actions(request)
        if not request.user.is_superuser:
            del actions['revert']
            del actions['export']
        return actions

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.aprobada is True:
            return ['talon', 'entidad', 'moneda', 'tasa', 'fecha', 'uuid', 'comercial', 'cuenta', 'forma', 'operacion',
                    'aprobada', 'subtotal_servicios', 'subtotal_productos', 'total', 'backup_bill', 'faltantes', 'nota']
        return self.readonly_fields

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',  # jquery

        )


class TalonAdmin(admin.ModelAdmin):
    list_display = ['numero_serie', 'descripcion', 'tipo', 'tipo_factura']
    list_display_links = ['numero_serie', 'descripcion', 'tipo', 'tipo_factura']


# registrar modelos en el sitio adminsitrativo
admin.site.register(Talon, TalonAdmin)
admin.site.register(Factura, FacturaAdmin)
# fin de registrar modelos en el sitio adminsitrativo
