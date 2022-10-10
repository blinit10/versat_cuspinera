from django.contrib import admin
from inventario.models import Producto


# InLines
# fin InLines
# ModelAdmin
# fin de ModelAdmin
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['sku', 'nombre', 'cantidad_inventario']
    list_display_links = ['sku', 'nombre', 'cantidad_inventario']
    readonly_fields = ['sku', 'nombre', 'cantidad_inventario', 'precio', 'precio_lb', 'um',
                       'proveedor',
                       'marca', 'subcategoria', 'descripcion', 'municipios',
                       'cantidad_inventario', 'visible', 'sku', 'upc', 'cantidad_maxima']
    fieldsets = (
        ('Información Básica', {
            'fields': (
                'sku', 'nombre', 'precio', 'precio_lb', 'um', 'upc')}),
        ('Información organizativa', {
            'fields': ('proveedor', 'marca', 'subcategoria', 'municipios', 'visible')}),
        ('Otros', {
            'fields': ('descripcion', 'cantidad_inventario','cantidad_maxima')}),
    )

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save': False,
            'show_save_and_continue': False,
            'show_delete': False,
            'show_save_and_add_another': False,

        })
        return super().render_change_form(request, context, add, change, form_url, obj)
# registrar modelos en el sitio adminsitrativo
admin.site.register(Producto, ProductoAdmin)
# fin de registrar modelos en el sitio adminsitrativo
