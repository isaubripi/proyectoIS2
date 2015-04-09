from django.conf.urls import patterns, include, url
from .views import UsuarioView, CrearUsuario, CrearUsuarioConfirm, EditarUsuario, EditarUsuarioConfirm, EliminarUsuario

urlpatterns= patterns('',
    url('^$', UsuarioView.as_view(), name='usuario'),
    url('^crear/$', CrearUsuario.as_view(), name='crear_usuario'),
    url('^crear/confirmar/$', CrearUsuarioConfirm.as_view(), name='creacion_usuario_confirmar'),
    url('^editar/$', EditarUsuario.as_view(), name='editar_usuario'),
    url('^editar/confirmar/$', EditarUsuarioConfirm.as_view(), name='editar_usuario_confirmar'),
    url('^eliminar/$', EliminarUsuario.as_view(), name='eliminar_usuario'),
    #url('^mostrar/$', MostrarUsuario.as_view(), name='mostrar_usuario'),
)



'''from django.conf.urls import patterns, include, url
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
)'''