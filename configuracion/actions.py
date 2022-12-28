from datetime import datetime
from django.contrib import admin
from django.http import HttpResponse
import locale

locale.setlocale(locale.LC_ALL, '')
from configuracion.models import DatosOrganizacion, Moneda


@admin.action(description='Exportar entidades')
def exportar(modeladmin, request, queryset):
    lines = []
    for entidad in queryset:
        if len(entidad.codigo) == 0:
            codigo = ' '
        else:
            codigo = entidad.codigo
        if len(entidad.nombre) == 0:
            nombre = ' '
        else:
            nombre = entidad.nombre
        if len(entidad.reeup) == 0:
            reeup = ' '
        else:
            reeup = entidad.reeup
        if len(entidad.abreviatura) == 0:
            abreviatura = ' '
        else:
            abreviatura = entidad.abreviatura
        if len(entidad.direccion) == 0:
            direccion = ' '
        else:
            direccion = entidad.direccion
        if len(entidad.correo) == 0:
            correo = ' '
        else:
            correo = entidad.correo
        if len(entidad.telefono) == 0:
            telefono = ' '
        else:
            telefono = entidad.telefono
        if len(entidad.nit) == 0:
            nit = ' '
        else:
            nit = entidad.nit
        if len(entidad.ircc) == 0:
            ircc = ' '
        else:
            ircc = entidad.ircc
        if len(entidad.provincia) == 0:
            provincia = ' '
        else:
            provincia = entidad.provincia
        if len(entidad.pais) == 0:
            pais = ' '
        else:
            pais = entidad.pais
        lines.append(
            "{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}".format(codigo, reeup, nombre, abreviatura, correo, telefono, nit,
                                                      direccion, ircc, provincia, pais))
    response_content = '\n'.join(lines)
    response = HttpResponse(response_content, content_type="text/plain,charset=utf8")
    response['Content-Disposition'] = 'attachment; filename={0}'.format('Entidades.cla')
    return response
