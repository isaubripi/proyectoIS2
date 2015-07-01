# -.- coding: utf-8 -.-
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

from django.utils import timezone
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


#La clase Login es la encargada de la primera vista del proyecto que es un formulario para logueo
class LoginView(TemplateView):
    template_name = 'login.html'
    def get(self, request, *args, **kwargs):
        return render(request,self.template_name)

@login_required(login_url='/')
def cerrar(request):
    logout(request)
    return HttpResponseRedirect('/')


class Recuperar(TemplateView):

    template_name = 'Recuperar.html'
    def post(self, request, *args, **kwargs):

        return render(request, self.template_name)


class RecuperarConfirm(TemplateView):

    template_name = 'RecuperarConfirm.html'

    def post(self, request, *args, **kwargs):

        diccionario = {}
        email = request.POST['email']

        Usuarios = Usuario.objects.filter(estado=True)
        existe= Usuario.objects.filter(email=request.POST['email'], estado=True)

        for u in Usuarios:
            if u.email == email:

                password = u.password

                email_context = {
                    'titulo': 'SISTEMA DE GESTION DE PROYECTOS AGILES SK',
                    'usuario': u.nombre,
                    'mensaje': 'Se le ha enviado su password. Le recomendamos que la cambie una vez que ingrese al sistema:\n'
                                    + '\nPASSWORD: ' + password

                }
                # se renderiza el template con el context
                email_html = render_to_string('email.html', email_context)

                # se quitan las etiquetas html para que quede en texto plano
                email_text = strip_tags(email_html)

                correo = EmailMultiAlternatives(
                    'Recuperacion de Password',  # Asunto
                    email_text,  # contenido del correo
                    'sistemaskmail@gmail.com',  # quien lo envía
                    [u.email],  # a quien se envía
                )

                # se especifica que el contenido es html
                correo.attach(email_html, 'text/html')
                # se envía el correo
                correo.send()

                diccionario['error']='El password ha sido enviado a su direccion de correo'
                return render(request, self.template_name, diccionario)

        if not len(existe):
            diccionario['error']='La direccion proporcionada no se encuentra en la base de datos del sistema'
            return render(request, self.template_name, diccionario)



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




