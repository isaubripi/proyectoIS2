from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


from views import LoginView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sistemask.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    #url(r'^$', LoginView.as_view(), name= 'login' ),
     #AUTENTICACION
    url(r'^$', LoginView.as_view(), name="login" ),
    #url(r'^$', 'sistemask.views.login_page', name="login"),
    #PROYECTO
    url(r'^proyecto/', include('adm_proyectos.urls')),

    #url(r'^', include('adm_usuarios.urls')),
    url(r'^', include('adm_roles.urls')),
    url(r'^salir/', 'sistemask.views.cerrar', name = "cerrar"),
    #url(r'^', include('adm_proyectos.urls')),


    #url(r'^ingresar/$','sistemask.views.ingresar'),

    url(r'^', include('adm_flujos.urls')),
    url(r'^sprint/', include('adm_sprints.urls')),
    url(r'^historia/', include('adm_historias')),

)


