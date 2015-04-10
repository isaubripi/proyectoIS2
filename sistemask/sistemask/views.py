__author__ = 'isidro'

from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import request
from django.views.generic import TemplateView, CreateView, ListView
from adm_usuarios.models import Usuario
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, render_to_response

from sistemask.forms import LoginForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout


#La clase Login es la encargada de la primera vista del proyecto que es un formulario para logueo
class LoginView(TemplateView):
    template_name = 'login.html'
    def get(self, request, *args, **kwargs):
        return render(request,self.template_name)


'''def login_page(request):
    message = None
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    #message = "Te has identificado de modo correcto"
                    return render(request, 'adm_proyectos/templates/Proyecto.html')

                else:
                    message = "Tu usuario esta inactivo"
            else:
                message = "Nombre de usuario y/o password incorrecto"

    else:
        form=LoginForm()

    return render_to_response('login1.html', {'message': message, 'form': form}, context_instance=RequestContext(request))'''


'''#@login_required(login_url='/proyecto')
def cerrar(request):
    logout(request)
    return HttpResponseRedirect('/')


def ingresar(request):
    message = None
    if request.method == "POST":
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    message = "Te has identificado de modo correcto"
                    return HttpResponseRedirect('/privado')

                else:
                    message = "Tu usuario esta inactivo"
            else:
                message = "Nombre de usuario y/o password incorrecto"

    else:
        formulario=AuthenticationForm()
    return render_to_response('login1.html', {'message': message, 'formulario': formulario}, context_instance=RequestContext(request))'''




