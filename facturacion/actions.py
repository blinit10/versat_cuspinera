import json
import os
from datetime import datetime
from pathlib import Path
from wsgiref.util import FileWrapper

import requests
from django.contrib import messages
from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
import locale
locale.setlocale(locale.LC_ALL, '')
from codificadores.models import CuentaBancaria
from configuracion.models import DatosOrganizacion, Moneda
from facturacion.exportador import render_pdf_view
from inventario.models import Producto


@admin.action(description='Aprobar facturas')
def aprove(modeladmin, request, queryset):
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
            if DatosOrganizacion.objects.all()[0].test:
                headers = {'Authorization': 'Token {}'.format(DatosOrganizacion.objects.all()[0].llave)}
                response = requests.post('http://127.0.0.1:9000/backend/inventario/', headers=headers,
                                         data=data)
            else:
                headers = {'Authorization': 'Token 07e3d4a91f7098ad03ab59eede7f5f29a2728a20'}
                response = requests.post(
                    '{}/backend/inventario/'.format(DatosOrganizacion.objects.all()[0].server),
                    headers=headers, data=data)
            json_results = response.json()
            bill.backup_bill = str(json_results['pk'])
            bill.faltantes = bill.faltantes + '\n ' + str(datetime.now().date()) + ' ' + str(
                datetime.now().hour) + ':' + str(datetime.now().minute) + ':' + str(datetime.now().second) \
                             + '\n Faltantes: \n'
            try:
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
    for bill in queryset:
        if bill.aprobada:
            if DatosOrganizacion.objects.all()[0].test:
                headers = {'Authorization': 'Token {}'.format(DatosOrganizacion.objects.all()[0].llave)}
                response = requests.post('http://127.0.0.1:9000/backend/inventario/revertir/', headers=headers,
                                         data={'flujo': int(bill.backup_bill)})
            else:
                headers = {'Authorization': 'Token 07e3d4a91f7098ad03ab59eede7f5f29a2728a20'}
                response = requests.post(
                    '{}/backend/inventario/revertir/'.format(DatosOrganizacion.objects.all()[0].server),
                    headers=headers, data={'flujo': int(bill.backup_bill)})

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


def excel_date(date1):
    temp = datetime(1899, 12, 30)
    delta = date1 - temp
    return float(delta.days) + (float(delta.seconds) / 86400)
from datetime import date

@admin.action(description='Generar PDF')
def export_pdf(modeladmin, request, queryset):
    for bill in queryset:
        cfg = DatosOrganizacion.objects.all()[0]
        bill.subtotal_productos = f"{bill.subtotal_productos:,.2f}"
        bill.subtotal_servicios = f"{bill.subtotal_servicios:,.2f}"
        bill.total = f"{bill.total:,.2f}"
        return render_pdf_view(request, json.dumps({}), cfg, bill)


@admin.action(description='Exportar facturas')
def export(modeladmin, request, queryset):
    for bill in queryset:
        if bill.aprobada == True:
            lines = []
            cfg = DatosOrganizacion.objects.all()[0]
            cfg.bill_number = cfg.bill_number + 1
            cfg.save()
            numer_of_zeroes = ''
            for i in range(7 - len(str(cfg.bill_number))):
                numer_of_zeroes = numer_of_zeroes + '0'
            bill_name = cfg.bill_format + str(numer_of_zeroes) \
                        + str(cfg.bill_number) + '.Fac'
            file_name = '{}'.format(bill_name)
            fecha = str(excel_date(datetime(year=bill.fecha.year, month=bill.fecha.month,
                                            day=bill.fecha.day, hour=0, minute=0, second=0)))
            if bill.moneda.tipo == 'contable':
                mc_currency = bill.moneda.nombre
                mc_account = bill.cuenta.cuenta
                om_currency = ' '
                om_account = ' '
            else:
                om_currency = bill.moneda
                om_account = bill.cuenta.cuenta
                mc_currency = 'CUBAN PESO'
                mc_account = ' '
            lines.append("Numero={}\n".format(str(bill_name).replace('.Fac', '')))
            if mc_currency == ' ':
                lines.append("MC={}\n".format(Moneda.objects.filter(tipo='contable')[0]))
            else:
                lines.append("MC={}\n".format(mc_currency))
            if om_currency == ' ':
                lines.append("OM={}\n".format(''))
            else:
                lines.append("OM={}\n".format(om_currency.nombre))
            lines.append("Fecha={}\n".format(fecha[:len(fecha) - 2]))
            lines.append("Entidad={}\n".format(bill.entidad.codigo))
            lines.append("Concepto={}\n".format(bill.concepto))
            lines.append("Comercial={}\n".format(bill.comercial.nombres_apellidos))
            lines.append("CtaBancoMC={}\n".format(mc_account))
            lines.append("CtaBancoOM={}\n".format(om_account))
            lines.append("Forma={}\n".format(bill.forma.forma))
            lines.append("Operacion={}\n".format(bill.operacion.descripcion))
            lines.append("Observacion={}\n".format(bill.nota))
            lines.append("MA={}\n".format(' '))
            lines.append("CtoArancel={}\n".format(' '))
            lines.append("PorcientoAra={}\n".format('0'))
            lines.append("Talon={}\n".format(bill.talon.numero_serie))
            lines.append("Contrato={}\n".format(''))
            lines.append("VtaCadena={}\n".format('0'))
            lines.append("NomHecho={}\n".format(bill.comercial.nombres_apellidos))
            lines.append("CargoHecho={}\n".format(bill.comercial.cargo))
            lines.append("CIHecho={}\n".format(bill.comercial.ci))
            lines.append("NomJA={}\n".format(' '))
            lines.append("CIJA={}\n".format(' '))
            lines.append("NomTra={}\n".format(' '))
            lines.append("Chapa={}\n".format(' '))
            lines.append("LicTra={}\n".format(' '))
            lines.append("CITra={}\n".format(' '))
            lines.append("NomCliente={}\n".format(' '))
            lines.append("CargoCliente={}\n".format(' '))
            lines.append("CICliente={}\n".format(' '))
            lines.append("[Propiedades]\n")
            lines.append("\n")
            lines.append("[Detalle]\n")
            for product in bill.productos_factura.all():
                lines.append(
                    "{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}\n".format(product.almacen.codigo, product.concepto,
                                                                         product.producto.sku, product.producto.um,
                                                                         product.cantidad, product.recargo,
                                                                         product.descuento, 0, 0, 0,
                                                                         product.importe,
                                                                         '', product.precio, 0))
            for service in bill.servicios_factura.all():
                lines.append(
                    "{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}\n".format('S', service.concepto,
                                                                         service.servicio.codigo,
                                                                         '$', service.cantidad, service.recargo,
                                                                         service.descuento, 0, 0, 0,
                                                                         service.importe,
                                                                         '', 0, 0))
            lines.append("[PieFirma]\n")
            bill.exportada_como = bill_name
            bill.save()
            response_content = ''.join(lines)
            response = HttpResponse(response_content, content_type="text/plain,charset=utf8")
            response['Content-Disposition'] = 'attachment; filename={0}'.format(file_name)
            return response
