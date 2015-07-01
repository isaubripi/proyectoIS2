from django.conf.urls import patterns, include, url


from django.contrib import admin
from django.conf import settings
admin.autodiscover()


from views import LoginView, Recuperar, RecuperarConfirm

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sistemask.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    #url(r'^$', LoginView.as_view(), name= 'login' ),
     #AUTENTICACION
    url(r'^$', LoginView.as_view(), name="login" ),
    url(r'^recuperar/', Recuperar.as_view(), name="recuperar"),

    url(r'^password/', RecuperarConfirm.as_view(), name="recuperar_confirm"),

    #url(r'^$', 'sistemask.views.login_page', name="login"),
    #PROYECTO
    url(r'^proyecto/', include('adm_proyectos.urls')),

    #url(r'^', include('adm_usuarios.urls')),
    url(r'^', include('adm_roles.urls')),
    url(r'^salir/', 'sistemask.views.cerrar', name = "cerrar"),

    url(r'^', include('adm_flujos.urls')),
    url(r'^sprint/', include('adm_sprints.urls')),
    url(r'^historia/', include('adm_historias.urls')),
    url(r'^actividad/', include('adm_actividades.urls')),
    url(r'^historia/tareas/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT})

)


