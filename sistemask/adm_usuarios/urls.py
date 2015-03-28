from django.conf.urls import patterns, include, url
from .views import inicio, RegistrarUsuario, ListarUsuario, CambioEstado, EditarUsuario, EditarUsuarioConfirmar, eliminar
from django.contrib import admin
admin.autodiscover()

urlpatterns= patterns('',
    url(r'^inicio/$', inicio.as_view(), name= 'menu_inicio'),
    url(r'^inicio/usuario/crear/$', RegistrarUsuario.as_view(), name= 'registrar_usuario'),
    url(r'^inicio/usuario/$', ListarUsuario.as_view(), name= 'listar_usuario'),
    url(r'^inicio/usuario/eliminar/$', eliminar.as_view(), name= 'eliminar_usuario'),
    url(r'^inicio/usuario/cambio_estado/$', CambioEstado.as_view(), name='cambio_estado'),
    url(r'^inicio/usuario/editar/$', EditarUsuario.as_view(), name='editar_usuario'),
    url(r'^inicio/usuario/editar/confirmar/$', EditarUsuarioConfirmar.as_view(), name='editar_usuario_confirmar'),
)