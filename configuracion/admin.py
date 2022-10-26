from django.contrib import admin
from configuracion.models import Entidad, Moneda, Sucursal, DatosOrganizacion, Unidad, Area, Trabajador, Almacen, \
    Custodio, Banco, Ejercicio, Periodo, ConceptoVenta


# InLines
class PeriodoInLine(admin.StackedInline):
    model = Periodo
    extra = 0
    min_num = 1

# fin InLines
# ModelAdmin
# fin de ModelAdmin
class EntidadAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'reeup']
    list_display_links = ['codigo', 'nombre', 'reeup']
    search_fields = ['codigo', 'nombre', 'reeup', 'abreviatura', 'direccion', 'correo', 'telefono', 'nit', 'ircc',
                     'provincia', 'pais']
    search_help_text = 'Se buscará en codigo, nombre, reeup, abreviatura, direccion, correo, telefono, nit, ircc,' \
                       ' provincia, pais'


class MonedaAdmin(admin.ModelAdmin):
    list_display = ['siglas', 'tipo', 'tasa', 'nombre']
    list_display_links = ['siglas', 'tipo', 'tasa', 'nombre']
    list_filter = ['tipo', ]


class SucursalAdmin(admin.ModelAdmin):
    list_display = ['numero', 'direccion']
    list_display_links = ['numero', 'direccion']


class DatosOrganizacionAdmin(admin.ModelAdmin):
    list_display = ['miniatura', 'nombre', 'organismo', 'telefono']
    list_display_links = ['miniatura', 'nombre', 'organismo', 'telefono']
    readonly_fields = ['miniatura', ]
    fieldsets = (
        ('Sistema', {
            'fields': ('key', 'server', 'test', ('bill_format', 'bill_number'), 'bills_dir')}),
        ('Información Básica', {
            'fields': (
                'codigo', 'nombre', 'organismo', 'telefono', 'direccion')}),
        ('Personas de Interés', {
            'fields': ('presidente', 'contador')}),
        ('Otros', {
            'fields': (('nit', 'ircc'),)}),
        ('Multimedia', {
            'fields': ('logotipo', 'miniatura')}),
    )

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return self.readonly_fields + ['key', 'server', 'test']
        return self.readonly_fields


class UnidadAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'correo', 'direccion']
    list_display_links = ['codigo', 'nombre', 'correo', 'direccion']


class AreaAdmin(admin.ModelAdmin):
    list_display = ['unidad', 'clave', 'descripcion', 'direccion']
    list_display_links = ['unidad', 'clave', 'descripcion', 'direccion']


class TrabajadorAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombres', 'primer_apellido', 'segundo_apellido', 'nro_indentidad']
    list_display_links = ['codigo', 'nombres', 'primer_apellido', 'segundo_apellido', 'nro_indentidad']
    fieldsets = (
        ('Información Básica', {
            'fields': (
                'codigo', 'nombres', ('primer_apellido', 'segundo_apellido'), 'nro_indentidad')}),
        ('Otros', {
            'fields': ('direccion', 'correo')}),
    )


class AlmacenAdmin(admin.ModelAdmin):
    list_display = ['unidad', 'codigo', 'nombre', 'jefe_almacen', 'direccion']
    list_display_links = ['unidad', 'codigo', 'nombre', 'jefe_almacen', 'direccion']


class BancoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre']
    list_display_links = ['codigo', 'nombre']


class EjercicioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'inicio', 'fin']
    list_display_links = ['nombre', 'inicio', 'fin']
    inlines = [PeriodoInLine,]

class ConceptoVentaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descripcion', 'concepto', 'en_experimento']
    list_display_links = ['codigo', 'descripcion', 'concepto', 'en_experimento']

class CustodioAdmin(admin.ModelAdmin):
    list_display = ['unidad', 'codigo', 'nombre']
    list_display_links = ['unidad', 'codigo', 'nombre']

    def changeform_view(self, request, obj_id, form_url, extra_context=None):
        extra_context = extra_context or {}
        trabajadores = Trabajador.objects.all()
        extra_context['trabajadores'] = trabajadores
        return super(CustodioAdmin, self).changeform_view(request, obj_id, form_url, extra_context=extra_context)

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',  # jquery

        )


# registrar modelos en el sitio adminsitrativo
admin.site.register(Entidad, EntidadAdmin)
admin.site.register(Moneda, MonedaAdmin)
admin.site.register(Sucursal, SucursalAdmin)
admin.site.register(DatosOrganizacion, DatosOrganizacionAdmin)
admin.site.register(Unidad, UnidadAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Trabajador, TrabajadorAdmin)
admin.site.register(Almacen, AlmacenAdmin)
admin.site.register(Custodio, CustodioAdmin)
admin.site.register(Banco, BancoAdmin)
admin.site.register(Ejercicio, EjercicioAdmin)
admin.site.register(ConceptoVenta, ConceptoVentaAdmin)
# fin de registrar modelos en el sitio adminsitrativo
