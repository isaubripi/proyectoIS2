__author__ = 'ruben'

from django.conf.urls import patterns, include, url
from .views import HistoriaView, CrearHistoria, CrearHistoriaConfirm, EditarHistoria, EditarHistoriaConfirm, EliminarHistoria

urlpatterns= patterns('',
    url(r'^historia/$', HistoriaView.as_view(), name = 'historia'),
    url(r'^historia/crear/$', CrearHistoria.as_view(), name = 'crear_historia'),
    url(r'^historia/crear/confirmar/$', CrearHistoriaConfirm.as_view(), name = 'crear_historia_confirmar'),
    url(r'^historia/editar/$', EditarHistoria.as_view(), name = 'editar_historia'),
    url(r'^historia/editar/confirmar/$', EditarHistoriaConfirm.as_view(), name = 'editar_historia_confirmar'),
    url(r'^historia/eliminar/$', EliminarHistoria.as_view(), name = 'eliminar_historia'),



    )