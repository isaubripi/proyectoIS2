__author__ = 'ruben'

from django.conf.urls import patterns, include, url
from .views import HistoriaView, CrearHistoria, CrearHistoriaConfirm, EditarHistoria, EditarHistoriaConfirm, EliminarHistoria, VerHistorial, CargarHoras, CargarHorasConfirm

urlpatterns= patterns('',
    url(r'^$', HistoriaView.as_view(), name = 'historia'),
    url(r'^crear/$', CrearHistoria.as_view(), name = 'crear_historia'),
    url(r'^crear/confirmar/$', CrearHistoriaConfirm.as_view(), name = 'crear_historia_confirmar'),
    url(r'^editar/$', EditarHistoria.as_view(), name = 'editar_historia'),
    url(r'^editar/confirmar/$', EditarHistoriaConfirm.as_view(), name = 'editar_historia_confirmar'),
    url(r'^eliminar/$', EliminarHistoria.as_view(), name = 'eliminar_historia'),
    url(r'^historial/$', VerHistorial.as_view(), name = 'historial_historia'),
    url(r'^horas/$', CargarHoras.as_view(), name = 'cargar_horas'),
    url(r'^horas/confirmar/$', CargarHorasConfirm.as_view(), name = 'cargar_horas_confirmar'),




    )