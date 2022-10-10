from django.contrib import admin
from codificadores.models import Cargo, Comercial, PersonalAutorizado, FormaPago, Operacion, CuentaBancaria, TipoTalon


#InLines
#fin InLines
#ModelAdmin
#fin de ModelAdmin
class ComercialAdmin(admin.ModelAdmin):
    list_display = ['nombres_apellidos', 'ci', 'cargo']
    list_display_links = ['nombres_apellidos', 'ci', 'cargo']
    list_filter = ['cargo',]
    search_fields = ['nombres_apellidos', 'ci']
    search_help_text = 'Se buscará en nombre, apellidos, ci'

class PersonalAutorizadoAdmin(admin.ModelAdmin):
    list_display = ['entidad', 'cargo','nombres_apellidos', 'ci']
    list_display_links = ['entidad', 'cargo','nombres_apellidos', 'ci']
    list_filter = ['cargo', 'entidad']
    search_fields = ['nombres_apellidos', 'ci']
    search_help_text = 'Se buscará en nombre, apellidos, ci'

class FormaPagoAdmin(admin.ModelAdmin):
    list_display = ['forma', 'tipo']
    list_display_links = ['tipo', 'forma']
    list_filter = ['tipo',]

class CuentaBancariaAdmin(admin.ModelAdmin):
    list_display = ['sucursal','cuenta', 'nombre','moneda','codigo_intercambio']
    list_display_links = ['sucursal','cuenta', 'nombre','moneda','codigo_intercambio']
    list_filter = ['sucursal',]

class TipoTalonAdmin(admin.ModelAdmin):
    list_display = ['codigo','descripcion', 'categoria']
    list_display_links = ['codigo','descripcion', 'categoria']
    list_filter = ['categoria',]

#registrar modelos en el sitio adminsitrativo
admin.site.register(Cargo)
admin.site.register(Comercial, ComercialAdmin)
admin.site.register(PersonalAutorizado, PersonalAutorizadoAdmin)
admin.site.register(FormaPago,FormaPagoAdmin)
admin.site.register(Operacion)
admin.site.register(CuentaBancaria, CuentaBancariaAdmin)
admin.site.register(TipoTalon, TipoTalonAdmin)
#fin de registrar modelos en el sitio adminsitrativo