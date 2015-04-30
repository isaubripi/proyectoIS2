from django.conf.urls import patterns, include, url
from .views import ActividadView, CrearActividad, CrearActividadConfirm, EliminarActividad, ModificarActividad, ModificarActividadConfirm, EstablecerSecuencia, EstablecerSecuenciaConfirm


urlpatterns= patterns('',
    url(r'^$', ActividadView.as_view(), name= 'actividad'),
    url(r'^crear/$', CrearActividad.as_view(), name = 'crear_actividad'),
    url(r'^crear/confirmar/$', CrearActividadConfirm.as_view(), name = 'crear_actividad_confirmar'),
    url(r'^eliminar/$', EliminarActividad.as_view(), name='eliminar_actividad'),
    url(r'^editar/$', ModificarActividad.as_view(), name='modificar_actividad'),
    url(r'^editar/confirmar/$',ModificarActividadConfirm.as_view(), name='modificar_actividad_confirm'),
    url(r'^secuencia/$',EstablecerSecuencia.as_view(), name='establecer_secuencia' ),
    url(r'^secuencia/confirmar/$',EstablecerSecuenciaConfirm.as_view(), name='establecer_secuencia_confirm' ),
    )