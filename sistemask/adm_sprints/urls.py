from django.conf.urls import patterns, include, url
from .views import SprintView, CrearSprint, CrearSprintConfirm, EliminarSprint, ModificarSprint, ModificarSprintConfirm, ActivarSprint

urlpatterns= patterns('',
    url(r'^$', SprintView.as_view(), name="sprint"),
    url(r'^crear/$', CrearSprint.as_view(), name="crear_sprint"),
    url(r'^crear/confirmar/$', CrearSprintConfirm.as_view(), name="confirmar_crear_sprint"),
    url(r'^eliminar/$', EliminarSprint.as_view(), name="eliminar_sprint"),
    url(r'^modificar/$', ModificarSprint.as_view(), name= "modificar_sprint"),
    url(r'^modificar/confirmar/$', ModificarSprintConfirm.as_view(), name= "modificar_sprint"),
    url(r'^activar/$', ActivarSprint.as_view(), name= "activar_sprint")

)
