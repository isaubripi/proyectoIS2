__author__ = 'ruben'

from django.conf.urls import patterns, include, url
from .views import FlujoView, CrearFlujo, CrearFlujoConfirm, EditarFlujo, EditarFlujoConfirm, EliminarFlujo


urlpatterns= patterns('',
    url(r'^inicio/flujo/$', FlujoView.as_view(), name = 'flujo'),
    url(r'^inicio/flujo/crear$', CrearFlujo.as_view(), name = 'crear_flujo'),
    url(r'^inicio/flujo/crear/confirmar$', CrearFlujoConfirm.as_view(), name = 'crear_flujo_confirmar'),
    url(r'^inicio/flujo/editar/$', EditarFlujo.as_view(), name = 'editar_flujo'),
    url(r'^inicio/flujo/editar/confirmar/$', EditarFlujoConfirm.as_view(), name = 'editar_flujo_confirmar'),
    url(r'^inicio/flujo/eliminar/$', EliminarFlujo.as_view(), name = 'eliminar_flujo'),




    )