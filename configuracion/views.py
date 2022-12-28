from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.
from configuracion.models import Trabajador, Custodio, Unidad, Entidad


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
                             'Se ha creado el custodio {} {} {} a partir de su ficha de trabajdor'.format(
                                 trabajador.nombres,
                                 trabajador.primer_apellido, trabajador.segundo_apellido))
    except:
        messages.add_message(request, messages.ERROR,
                             'No se ha podido crear el custodio a partir de su ficha de trabajador.')
    return redirect('/admin/configuracion/custodio/')


def importar_entidades(request):
    if request.method == 'POST':
        archivo = request.FILES['entidades'].read()
        archivo = archivo.decode("ISO-8859-1")
        for line in str(archivo).splitlines():
            valores = line.split('|')
            try:
                try:
                    entidad = Entidad.objects.get(codigo=valores[0])
                    entidad.reeup = valores[1]
                    entidad.nombre = valores[2]
                    entidad.abreviatura = valores[3]
                    entidad.correo = valores[4]
                    entidad.telefono = valores[5]
                    entidad.nit = valores[6]
                    entidad.direccion = valores[7]
                    entidad.ircc = valores[8]
                    entidad.provincia = valores[9]
                    entidad.pais = valores[10]
                except:
                    entidad = Entidad(codigo=valores[0], nombre=valores[2], direccion=valores[7],
                                      abreviatura=valores[3], correo=valores[4], telefono=valores[5],
                                      provincia=valores[9], pais=valores[10], nit=valores[6], reeup=valores[2],
                                      ircc=valores[8])
                entidad.save()
            except:
                messages.add_message(request, messages.ERROR,
                                     'Formato incorrecto')
                return redirect('/configuracion/importar/entidades/')
        messages.add_message(request, messages.SUCCESS,
                             'Entidades Actualizadas')
        return redirect('/admin/configuracion/entidad/')
    return render(request, 'entidades_importar.html', {})
