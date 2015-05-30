__author__ = 'isidro'

from django.conf.urls import patterns, include, url
from .views import ProyectoView, EliminarProyecto, CrearProyecto, CrearProyectoConfirm, InicializarProyecto, InicializarProyectoConfirm, Ingresar, ModificarProyecto, ModificarProyectoConfirm, Generarkanban, ProductBacklog, ProductBacklogPri, ProductBacklogNeg, ProductBacklogTec, ReleaseHistoria, CancelarHistoria

urlpatterns= patterns('',
    url(r'^$', ProyectoView.as_view(), name="proyecto"),
    url(r'^crear/$', CrearProyecto.as_view(), name="crear_proyecto"),
    url(r'^crear/confirmar/$', CrearProyectoConfirm.as_view(), name="confirmar_crear_proyecto"),
    url(r'^eliminar/$', EliminarProyecto.as_view(), name="eliminar_proyecto"),
    #url(r'^informe/$', InformeProyecto.as_view(), name="informe_proyecto"),
    #url(r'^informe/$', InformeProyecto.as_view(), name="informe_proyecto"),
    url(r'^inicializar/$', InicializarProyecto.as_view(), name="inicializar_proyecto"),
    url(r'^inicializar/confirmar/$', InicializarProyectoConfirm.as_view(), name="inicializar_proyecto_confirmar"),
    #url(r'^salir/$', 'adm_proyectos.views.cerrar', name = 'salir'),
    url(r'^ingresar/$', Ingresar.as_view(), name="ingresar"),
    url(r'^modificar/$', ModificarProyecto.as_view(), name= "modificar_proyecto"),
    url(r'^modificar/confirmar/$', ModificarProyectoConfirm.as_view(), name= "modificar_proyecto"),
     #Usuarios
    url(r'^kanban/$',Generarkanban.as_view(), name='ver_kanban' ),
    url(r'^productbacklog/$',ProductBacklog.as_view(), name='ver_productbacklog' ),
    url(r'^productbacklogPri/$',ProductBacklogPri.as_view(), name='ver_productbacklog' ),
    url(r'^productbacklogNeg/$',ProductBacklogNeg.as_view(), name='ver_productbacklog' ),
    url(r'^productbacklogTec/$',ProductBacklogTec.as_view(), name='ver_productbacklog' ),
    url(r'^release/$',ReleaseHistoria.as_view(), name='release_historia' ),
    url(r'^cancelar/$',CancelarHistoria.as_view(), name='cancelar_historia' ),
    url(r'^usuario/', include('adm_usuarios.urls')),

)


