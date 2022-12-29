from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect, render
import requests

from configuracion.models import DatosOrganizacion, ProveedorPropio
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
    proveedores = ProveedorPropio.objects.values_list('nombre')
    for json_product in json_products['data']:
        if (str(json_product['proveedor']['nombre']),) in proveedores:
            locations = ""
            for location in json_product['municipios']:
                if locations != "":
                    locations = locations + ", " + str(location['nombre'])
                else:
                    locations = str(location['nombre'])
            product = Producto(sku=json_product['sku'] or json_product['slug'], nombre=json_product['nombre_versat'],
                               precio=json_product['precio'],
                               precio_lb=json_product['precioxlibra'], um=json_product['um'] or 'No especificada',
                               proveedor=json_product['proveedor']['nombre'], marca=json_product['marca']['nombre'],
                               subcategoria=json_product['subcategoria'], descripcion=json_product['descripcion'],
                               municipios=locations, cantidad_inventario=json_product['cant_inventario'],
                               visible=True, upc=json_product['upc'] or 'No especificado',
                               cantidad_maxima=json_product['max'], imagen=json_product['img_principal'],
                               precio_b2b=json_product['precio_b2b'])
            if len(Producto.objects.filter(sku=product.sku)) == 0:
                product.save()
                actual_products.append(product.sku)
            else:
                existing_product = product
                existing_product.save()
    messages.add_message(request, messages.SUCCESS,
                         'Se han actualizado con éxito los productos')
    return redirect('/admin/inventario/producto/')
