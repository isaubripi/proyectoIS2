from django.conf.urls import patterns, include, url
from .views import UsuarioView, CrearUsuario, CrearUsuarioConfirm, EditarUsuario, EditarUsuarioConfirm, EliminarUsuario, AsignarRoles, AsignarRolesConfirm, CreaRol, CreaRolConfirm, EditaRol, EditaRolConfirm, EliminaRol, GestionarRol

urlpatterns= patterns('',
    url('^$', UsuarioView.as_view(), name='usuario'),
    url('^crear/$', CrearUsuario.as_view(), name='crear_usuario'),
    url('^crear/confirmar/$', CrearUsuarioConfirm.as_view(), name='creacion_usuario_confirmar'),
    url('^editar/$', EditarUsuario.as_view(), name='editar_usuario'),
    url('^editar/confirmar/$', EditarUsuarioConfirm.as_view(), name='editar_usuario_confirmar'),
    url('^eliminar/$', EliminarUsuario.as_view(), name='eliminar_usuario'),
    url('^asignar/$', AsignarRoles.as_view(), name='asignar_roles'),
    url('^asignar/confirmar/$', AsignarRolesConfirm.as_view(), name='asignar_roles_confirmar'),
    url('^crearrol/$', CreaRol.as_view(), name='crea_roles'),
    url('^crearrol/confirmar/$', CreaRolConfirm.as_view(), name='crea_roles_confirmar'),
    url('^editarrol/$', EditaRol.as_view(), name='edita_roles'),
    url('^editarrol/confirmar/$', EditaRolConfirm.as_view(), name='edita_roles_confirmar'),
    url('^eliminarrol/$', EliminaRol.as_view(), name='elimina_roles'),
    url('^gestionarrol/$', GestionarRol.as_view(), name='gestionar_roles'),


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