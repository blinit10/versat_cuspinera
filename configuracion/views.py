from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.
from configuracion.models import Trabajador, Custodio, Unidad


def crear_custodio_trabajador(request, codigo_trabajador, codigo_unidad):
    try:
        trabajador = Trabajador.objects.get(codigo=codigo_trabajador)
        unidad = Unidad.objects.get(codigo=codigo_unidad)
        if len(Custodio.objects.filter(codigo=trabajador.codigo)) > 0:
            messages.add_message(request, messages.WARNING,
                                 'Ya existe un custodio basado en ese trabajador, o con ese mismo código.')
            return redirect('/admin/configuracion/custodio/')
        custodio = Custodio(codigo=trabajador.codigo, unidad=unidad, nombre=trabajador.nombres)
        custodio.save()
        messages.add_message(request, messages.SUCCESS,
                             'Se ha creado el custodio {} {} {} a partir de su ficha de trabajdor'.format(trabajador.nombres,
                                                            trabajador.primer_apellido, trabajador.segundo_apellido))
    except:
        messages.add_message(request, messages.ERROR,
                             'No se ha podido crear el custodio a partir de su ficha de trabajador.')
    return redirect('/admin/configuracion/custodio/')
