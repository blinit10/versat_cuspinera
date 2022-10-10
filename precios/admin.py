from django.contrib import admin
from precios.models import Servicio


# InLines
# fin InLines
# ModelAdmin
# fin de ModelAdmin
class ServicioAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descripcion', 'um']
    list_display_links = ['codigo', 'descripcion', 'um']

# registrar modelos en el sitio adminsitrativo
admin.site.register(Servicio, ServicioAdmin)
# fin de registrar modelos en el sitio adminsitrativo