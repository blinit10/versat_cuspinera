from django.urls import path

from inventario.views import actualizar_sistema

urlpatterns = [
    path('actualizar/', actualizar_sistema, name='actualizar_sistema'),
]