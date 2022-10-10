from datetime import datetime

import requests
from django.contrib import messages
from django.contrib import admin

from inventario.models import Producto


@admin.action(description='Aprobar facturas')
def aprove(modeladmin, request, queryset):
    headers = {'Authorization': 'Token 2a95bf33d7409826929ab18c3891b069ef7c7019'}
    data = {}
    for bill in queryset:
        if not bill.aprobada:
            if bill.nota is not None:
                note = bill.nota
                data['nota'] = note
            else:
                data['nota'] = ""
            for service in bill.servicios_factura.all():
                data['nota'] = data['nota'] + '\n ' + str(
                    service.cantidad) + 'x ' + service.servicio.descripcion + ' - ' \
                                                                              '' + str(service.importe) + ' ' + str(
                    service.factura.moneda)

            for product in bill.productos_factura.all():
                data[str(product.producto.sku)] = product.cantidad
            response = requests.post('http://127.0.0.1:9000/backend/inventario/', headers=headers, data=data)
            json_results = response.json()
            bill.backup_bill = str(json_results['pk'])
            try:
                bill.faltantes = bill.faltantes + '\n ' + str(datetime.now().date()) + ' ' + str(
                    datetime.now().hour) + ':' + str(datetime.now().minute) + ':' + str(datetime.now().second) \
                                 + ' Faltantes: \n'
                for json_resto in json_results['restos']:
                    bill.faltantes = bill.faltantes + Producto.objects.get(sku=json_resto['sku']).nombre + ' - ' \
                                     + str(json_resto['cantidad']) + '\n'
                bill.faltantes = bill.faltantes + '----------------------------------------------------------' \
                                                  '--------------------' \
                                                  '-----------------------------------------------------------' \
                                                  '------------- \n'
            except:
                pass
            bill.aprobada = True
            bill.save()
    messages.add_message(request, messages.INFO,
                         'Se aprobaron las facturas seleccionadas')


@admin.action(description='Revertir facturas')
def revert(modeladmin, request, queryset):
    headers = {'Authorization': 'Token 2a95bf33d7409826929ab18c3891b069ef7c7019'}
    for bill in queryset:
        if bill.aprobada:
            response = requests.post('http://127.0.0.1:9000/backend/inventario/revertir/', headers=headers,
                                     data={'flujo': int(bill.backup_bill)})
            bill.faltantes = bill.faltantes + '\n ' + str(datetime.now().date()) + ' ' + str(
                datetime.now().hour) + ':' + str(datetime.now().minute) + ':' + str(datetime.now().second) \
                             + ' Se revirtió esta factura \n'
            bill.faltantes = bill.faltantes + '-----------------------------------------------------------' \
                                                  '-------------------' \
                                                  '-----------------------------------------------------------' \
                                                  '-------------  \n'
            bill.aprobada = False
            bill.save()
    messages.add_message(request, messages.INFO,
                         'Se revirtieron las facturas seleccionadas')
