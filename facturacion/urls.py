from django.urls import path

from facturacion.views import *

urlpatterns = [
    path('scanner/', factura_scanner, name='factura_scanner'),
    path('scanner/stream/', factura_scanner_scan, name='factura_scanner_scan'),
    path('scanner/facturar/', facturar, name='facturar'),
]