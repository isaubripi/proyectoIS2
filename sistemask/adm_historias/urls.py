__author__ = 'ruben'

from django.conf.urls import patterns, include, url
from .views import HistoriaView, CrearHistoria, CrearHistoriaConfirm, EditarHistoria, EditarHistoriaConfirm, EliminarHistoria

urlpatterns= patterns('',
    url(r'^$', HistoriaView.as_view(), name = 'historia'),
    url(r'^crear/$', CrearHistoria.as_view(), name = 'crear_historia'),
    url(r'^crear/confirmar/$', CrearHistoriaConfirm.as_view(), name = 'crear_historia_confirmar'),
    url(r'^editar/$', EditarHistoria.as_view(), name = 'editar_historia'),
    url(r'^editar/confirmar/$', EditarHistoriaConfirm.as_view(), name = 'editar_historia_confirmar'),
    url(r'^eliminar/$', EliminarHistoria.as_view(), name = 'eliminar_historia'),



    )