from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from views import login

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sistemask.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', login.as_view(), name= 'login' ),
    url(r'^', include('adm_usuarios.urls')),
    url(r'^', include('adm_roles.urls')),


)
