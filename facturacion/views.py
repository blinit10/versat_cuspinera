import datetime

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
import cv2
import numpy as np
from time import sleep
from tkinter import *
from pyzbar import pyzbar

# Create your views here.
from codificadores.models import CuentaBancaria, FormaPago, Operacion, Comercial
from configuracion.models import DatosOrganizacion, Entidad, Moneda, Almacen
from facturacion.models import Talon, Factura, ComponenteProductoFactura
from inventario.models import Producto


def factura_scanner(request):
    talones = Talon.objects.all()
    entidades = Entidad.objects.all()
    monedas = Moneda.objects.all()
    cuentas = CuentaBancaria.objects.all()
    formas = FormaPago.objects.all()
    operaciones = Operacion.objects.all()
    almacenes = Almacen.objects.all()
    return render(request, 'factura_scanner.html', {'talones': talones, 'entidades': entidades, 'monedas': monedas,
                                                    'cuentas': cuentas, 'formas': formas, 'operaciones': operaciones,
                                                    'almacenes':almacenes})


def factura_scanner_scan(request):
    try:
        capture = cv2.VideoCapture("{}".format(str(request.GET.get('ruta'))))
        while (True):
            ret, frame = capture.read()
            # cv2.imshow('Frame', frame)
            # if cv2.waitKey(25) & 0xFF == ord('q'):
            #     break
            barcodes = pyzbar.decode(frame)
            for barcode in barcodes:
                barcode_info = barcode.data.decode('utf-8')
                print(barcode_info)
                producto = Producto.objects.filter(upc=barcode_info)[0]
                producto = {'nombre': producto.nombre, 'img': producto.imagen, 'precio': producto.precio,
                            'precio_b2b': producto.precio_b2b, 'upc': producto.upc}
                capture.release()
                cv2.destroyAllWindows()
                return JsonResponse(data={'bar_code': producto}, safe=False)
    except:
        return JsonResponse(data={'bar_code': '#!ERROR'}, safe=False)


def actualizar_componente(factura, componente, producto):
    componente.producto = producto
    componente.factura = factura
    componente.precio = producto.precio
    componente.recargo = 0
    componente.descuento = 0

def facturar(request):
    # 'ci': ['96100808269']
    # 'talon': ['001']
    # 'moneda': ['USD::24,0::otras']
    # 'fecha': ['2022-12-21T08:39']
    # 'cuenta-bancaria': ['0524145000171216']
    # 'forma': ['Tranferencia']
    # 'operacion': ['1']
    # 'cantidad': ['1']
    # '0078000002744-precio': ['0.99']
    # '0078000001969-precio': ['0.8']#
    print(request.POST)
    try:
        comercial = Comercial.objects.get(ci=request.POST['ci'])
    except:
        messages.add_message(request, messages.ERROR,
                             'No se encontró ninguna comercial con ese CI')
        return redirect('/facturacion/scanner/')
    try:
        almacen = Almacen.objects.get(codigo=request.POST['almacen'])
    except:
        messages.add_message(request, messages.ERROR,
                             'No existe el almacén')
        return redirect('/facturacion/scanner/')
    try:
        entidad = Entidad.objects.get(codigo=request.POST['entidad'])
    except:
        messages.add_message(request, messages.ERROR,
                             'No existe la entidad')
        return redirect('/facturacion/scanner/')
    try:
        talon = Talon.objects.get(numero_serie=request.POST['talon'])
    except:
        messages.add_message(request, messages.ERROR,
                             'No existe ese Talón')
        return redirect('/facturacion/scanner/')
    try:
        cuenta = CuentaBancaria.objects.get(cuenta=request.POST['cuenta-bancaria'])
    except:
        messages.add_message(request, messages.ERROR,
                             'No existe esa Cuenta Bancaria')
        return redirect('/facturacion/scanner/')
    try:
        forma = FormaPago.objects.get(forma=request.POST['forma'])
    except:
        messages.add_message(request, messages.ERROR,
                             'No existe esa Forma de Pago')
        return redirect('/facturacion/scanner/')
    try:
        operacion = Operacion.objects.get(pk=int(request.POST['operacion']))
    except:
        messages.add_message(request, messages.ERROR,
                             'No existe esa Operación')
        return redirect('/facturacion/scanner/')
    try:
        moneda = Moneda.objects.get(tipo=str(request.POST['moneda']).split('::')[2],
                                    siglas=str(request.POST['moneda']).split('::')[0])
    except:
        messages.add_message(request, messages.ERROR,
                             'No existe esa Operación')
    factura = Factura(fecha=request.POST['fecha'], operacion=operacion, forma=forma, cuenta=cuenta, talon=talon,
                      comercial=comercial, entidad=entidad, moneda=moneda)
    factura.save()
    productos = {}
    for key in request.POST:
        print('Key: {}, Value: {}'.format(key, request.POST[key]))
        if key != 'csrfmiddlewaretoken' and key != 'ruta' and key != 'ci' and key != 'talon' and \
                key != 'moneda' and key != 'fecha' and key != 'cuenta-bancaria' and key != 'forma' and\
                key != 'operacion' and key != 'cantidad' and key != 'entidad' and key != 'almacen':
            try:
                upc = str(key).replace('-cantidadinput', '')
                producto = Producto.objects.get(upc=upc)
                if upc not in productos:
                    productos[upc] = {'cantidad':int(request.POST[key])}
                else:
                    productos[upc].update({'cantidad':int(request.POST[key])})
            except:
                upc = str(key).replace('-precio', '')
                producto = Producto.objects.get(upc=upc)
                if upc not in productos:
                    productos[upc] = {'precio':request.POST[key]}
                else:
                    productos[upc].update({'precio':request.POST[key]})
    for key in productos:
        print(key)
        producto = Producto.objects.get(upc=key)
        componente = ComponenteProductoFactura(factura=factura, producto=producto, concepto='004',
                                               almacen=almacen, recargo=0, descuento=0,
                                               precio=producto.precio, importe=productos[key]['precio'],
                                               cantidad=productos[key]['cantidad'])
        componente.save()
    messages.add_message(request, messages.SUCCESS,
                         'Pre-Factura creada')
    return redirect('/admin/facturacion/factura/{}/change/'.format(factura.uuid))
