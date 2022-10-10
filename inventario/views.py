from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect, render
import requests

from configuracion.models import DatosOrganizacion
from inventario.models import Producto


@transaction.atomic
def actualizar_sistema(request):
    if DatosOrganizacion.objects.all()[0].test:
        headers = {'Authorization': 'Token {}'.format(DatosOrganizacion.objects.all()[0].llave)}
        response = requests.get('http://127.0.0.1:9000/backend/inventario/', headers=headers)
    else:
        headers = {'Authorization': 'Token 07e3d4a91f7098ad03ab59eede7f5f29a2728a20'}
        response = requests.get('{}/backend/inventario/'.format(DatosOrganizacion.objects.all()[0].server), headers=headers)
    json_products = response.json()
    actual_products = []
    for json_product in json_products['data']:
        locations = ""
        for location in json_product['municipios']:
            if locations != "":
                locations = locations + ", " + str(location['nombre'])
            else:
                locations = str(location['nombre'])
        product = Producto(sku=json_product['sku'] or json_product['slug'], nombre=json_product['nombre'],
                           precio=json_product['precio'],
                           precio_lb=json_product['precioxlibra'], um=json_product['um'] or 'No especificada',
                           proveedor=json_product['proveedor']['nombre'], marca=json_product['marca']['nombre'],
                           subcategoria=json_product['subcategoria'], descripcion=json_product['descripcion'],
                           municipios=locations, cantidad_inventario=json_product['cant_inventario'],
                           visible=True, upc=json_product['upc'] or 'No especificado',
                           cantidad_maxima=json_product['max'])
        if len(Producto.objects.filter(sku=product.sku)) == 0:
            product.save()
            actual_products.append(product.sku)
        else:
            existing_product = product
            existing_product.save()
    messages.add_message(request, messages.SUCCESS,
                         'Se han actualizado con éxito los productos')
    return redirect('/admin/inventario/producto/')


def iframe_test(request):
    url = "http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso"
    payload = """<?xml version="1.0" encoding="UTF-8"?>
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
        <soapenv:Header>
         <wsse:Security soapenv:mustUnderstand="1" 
        xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-s
        ecext-1.0.xsd">
         <wsse:UsernameToken>
         <wsse:Username>yourMerchantID</wsse:Username>
         <wsse:Password 
        Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-pro
        file-1.0#PasswordText">yourPassword</wsse:Password>
         </wsse:UsernameToken>
         </wsse:Security>
         </soapenv:Header>
         <soapenv:Body>
         <requestMessage xmlns="urn:schemas-cybersource-com:transaction-data-N.NN">
         <merchantID>diplomarket0001</merchantID>
         <merchantReferenceCode>MRC-123</merchantReferenceCode>
         <billTo>
         <firstName>John</firstName>
         <lastName>Doe</lastName>
         <street1>1295 Charleston Road</street1>
         <city>Mountain View</city>
         <state>CA</state>
         <postalCode>94043</postalCode>
         <country>US</country>
         <email>null@cybersource.com</email>
         </billTo>
         <item id="0">
         <unitPrice>5.00</unitPrice>
        Configuring SOAP Toolkits for Web Services | 5
         <quantity>1</quantity>
         </item>
         <item id="1">
         <unitPrice>10.00</unitPrice>
         <quantity>2</quantity>
         </item>
         <purchaseTotals>
         <currency>USD</currency>
         </purchaseTotals>
         <card>
         <accountNumber>4111111111111111</accountNumber>
         <expirationMonth>11</expirationMonth>
         <expirationYear>2020</expirationYear>
         </card>
         <ccAuthService run="true"/>
         </requestMessage>
         </soapenv:Body>
        </soapenv:Envelope>"""
    #Key 5b7ac22d-f8f6-43ac-a611-e93de7061716
    #Shared secret key S6jo9V0+wJsgEz51Kxn7bpvFe3zviLaziUQN9jUWvn4=

    return render(request, 'test.html', {})
