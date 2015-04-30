__author__ = 'ruben'

from django.conf.urls import patterns, include, url
from .views import FlujoView, CrearFlujo, CrearFlujoConfirm, EditarFlujo, EditarFlujoConfirm, EliminarFlujo


urlpatterns= patterns('',
    url(r'^flujo/$', FlujoView.as_view(), name = 'flujo'),
    url(r'^flujo/crear/$', CrearFlujo.as_view(), name = 'crear_flujo'),
    url(r'^flujo/crear/confirmar/$', CrearFlujoConfirm.as_view(), name = 'crear_flujo_confirmar'),
    url(r'^flujo/editar/$', EditarFlujo.as_view(), name = 'editar_flujo'),
    url(r'^flujo/editar/confirmar/$', EditarFlujoConfirm.as_view(), name = 'editar_flujo_confirmar'),
    url(r'^flujo/eliminar/$', EliminarFlujo.as_view(), name = 'eliminar_flujo'),
    #url(r'^flujo/actividades/$', Actividades.as_view(), name = 'actividades_flujo'),




    )