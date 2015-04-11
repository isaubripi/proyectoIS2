from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Flujo
from adm_proyectos.models import Proyecto
from adm_usuarios.models import Usuario
# Create your views here.


class FlujoView(TemplateView):

    '''
    Esta clase muestra los flujos en el proyecto.

    Hereda de TemplateView.

    template_name es el archivo html de esta clase.
    '''

    template_name = 'Flujo.html'
    def post(self, request, *args, **kwargs):
        '''
        Esta funcion tiene los parametros:
        :param request:
        :param args:
        :param kwargs:
        :return: request, el arhivo html y el diccionario.
        '''
        diccionario={}
        #usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        #proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        #diccionario['logueado']= usuario_logueado
        #diccionario['proyecto']= proyecto_actual


        lista = Flujo.objects.filter(activo=True)
        diccionario['lista']=lista
        return render(request, self.template_name, diccionario)


class CrearFlujo(FlujoView):
    '''
    Esta clase crea los flujos en el proyecto.

    Hereda de FlujoView.

    template_name es el archivo html de esta clase.
    '''

    template_name = 'CrearFlujo.html'

    def post(self, request, *args, **kwargs):

        '''
        Esta funcion tiene los parametros:

        :param request:
        :param args:
        :param kwargs:
        :return: request, el archivo html y el diccionario
        '''
        diccionario={}
        #usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        #proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        #diccionario['logueado']= usuario_logueado
        #diccionario['proyecto']= proyecto_actual


        return render(request, self.template_name, diccionario)

class CrearFlujoConfirm(CrearFlujo):

    '''
    Esta clase confirma la creacion de los flujos en el proyecto.

    Hereda de CrearFlujo

    template_name es el archivo html de esta clase.
    '''

    template_name = 'CrearFlujoConfirmar.html'
    def post(self, request, *args, **kwargs):
        '''
        Esta funcion tiene los parametros:

        :param request:
        :param args:
        :param kwargs:
        :return: request y el archivo html
        Si se introduce un nombre de flujo que ya existe lanza el error.
        '''

        flujo_nombre= request.POST['nombre_flujo']
        flujo_descripcion= request.POST['descripcion_flujo']
        flujo_proyecto= request.POST['proyecto_flujo']

        if len(Flujo.objects.filter(nombre= flujo_nombre, activo= True)):
            error = "Nombre del flujo ya existe. Intente otro nombre"
            return render(request, super(CrearFlujoConfirm, self).template_name, {'error':error})
        nuevo_flujo = Flujo(nombre= flujo_nombre, descripcion= flujo_descripcion, activo=True)


        nuevo_flujo.save()

        return render(request, self.template_name)

class EditarFlujo(FlujoView):
    '''
    Esta clase edita flujos en el proyecto.

    Hereda de FlujoView

    template_name es el archivo html de esta clase.
    '''

    template_name = 'EditarFlujo.html'

    def post(self, request, *args, **kwargs):
        '''
        Esta funcion tiene los parametros:
        :param request:
        :param args:
        :param kwargs:
        :return: request, el archivo html y el diccionario.
        '''
        diccionario={}
        #usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        #proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        #diccionario['logueado']= usuario_logueado
        #diccionario['proyecto']= proyecto_actual

        flujo_actual = Flujo.objects.get(id= request.POST['flujo'])
        diccionario['flujo']=flujo_actual

        return render(request, self.template_name, diccionario)


class EditarFlujoConfirm(EditarFlujo):
    '''
    Esta clase confirma la modificacion de los flujos en el proyecto.

    Hereda de EditarFlujo

    template_name es el archivo html de esta clase.
    '''

    template_name = 'EditarFlujoConfirmar.html'

    def post(self, request, *args, **kwargs):
        '''
        Esta funcion tiene los parametros:
        :param request:
        :param args:
        :param kwargs:
        :return: request y el archivo html.
        '''

        flujo_editado = Flujo.objects.get(nombre= request.POST['nombre_flujo'])
        nuevo_flujo_nombre = request.POST['nombre_nuevo_flujo']
        nuevo_flujo_descripcion = request.POST['descripcion_nuevo_flujo']
        flujo_editado.nombre = nuevo_flujo_nombre
        flujo_editado.descripcion = nuevo_flujo_descripcion
        flujo_editado.save()

        return render(request, self.template_name)

class EliminarFlujo(FlujoView):
    '''
    Esta clase elimina flujos en el proyecto.

    Hereda de FlujoView

    template_name es el archivo html de esta clase.
    '''

    template_name = 'EliminarFlujo.html'

    def post(self, request, *args, **kwargs):
        '''
        Esta funcion tiene los parametros:
        :param request:
        :param args:
        :param kwargs:
        :return: request, el archivo html y el diccionario.
        '''

        diccionario={}
        #usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        #proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        #diccionario['logueado']= usuario_logueado
        #diccionario['proyecto']= proyecto_actual

        flujo = Flujo.objects.get(id = request.POST['flujo'])

        flujo.activo = False

        flujo.save()

        return render(request, self.template_name, diccionario)


class Actividades(TemplateView):
    '''
    Esta clase va a permitir agregar actividades a los flujos en el proyecto.

    Hereda de TemplateView

    template_name es el archivo html de esta clase.
    '''
    template_name = 'Actividades.html'
    def post(self, request, *args, **kwargs):
        '''
        Esta funcion emite el mensaje: En construccion. Tiene los parametros:
        :param request:
        :param args:
        :param kwargs:
        :return: request y el archivo html.
        '''
        return render(request, self.template_name)

