from django.urls import path

from configuracion.views import crear_custodio_trabajador

urlpatterns = [
    path('custodio/<codigo_trabajador>/<codigo_unidad>/', crear_custodio_trabajador, name='crear_custodio_trabajador'),
]