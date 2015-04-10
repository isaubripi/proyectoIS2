from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Flujo
# Create your views here.


class FlujoView(TemplateView):

    template_name = 'Flujo.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual


        lista = Flujo.objects.filter(activo=True, proyecto=proyecto_actual.id)
        diccionario['lista']=lista
        return render(request, self.template_name, diccionario)


class CrearFlujo(FlujoView):

    template_name = 'CrearFlujo.html'

    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual


        return render(request, self.template_name, diccionario)

class CrearFlujoConfirm(CrearFlujo):

    template_name = 'CrearFlujoConfirmar.html'
    def post(self, request, *args, **kwargs):

        flujo_nombre= request.POST['nombre_flujo']
        flujo_descripcion= request.POST['descripcion_flujo']
        if len(Flujo.objects.filter(nombre= flujo_nombre, activo= True)):
            error = "Nombre del flujo ya existe. Intente otro nombre"
            return render(request, super(CrearFlujoConfirm, self).template_name, {'error':error})
        nuevo_flujo = Flujo(nombre= flujo_nombre, descripcion= flujo_descripcion)


        nuevo_flujo.save()

        return render(request, self.template_name)

class EditarFlujo(FlujoView):

    template_name = 'EditarFlujo.html'

    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual

        flujo_actual = Flujo.objects.get(id= request.POST['flujo'])
        diccionario['flujo']=flujo_actual

        return render(request, self.template_name, diccionario)


class EditarFlujoConfirm(EditarFlujo):

    template_name = 'EditarFlujoConfirmar.html'

    def post(self, request, *args, **kwargs):

        flujo = Flujo.objects.filter(nombre= request.POST['nombre_flujo'])
        nuevo_flujo_nombre = request.POST['nombre_nuevo_flujo']
        nuevo_flujo_descripcion = request.POST['descripcion_nuevo_flujo']
        flujo.nombre = nuevo_flujo_nombre
        flujo.descripcion = nuevo_flujo_descripcion
        flujo.save()

        return render(request, self.template_name)

class EliminarFlujo(FlujoView):

    template_name = 'EliminarFlujo.html'

    def post(self, request, *args, **kwargs):

        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual

        flujo = Flujo.objects.get(id = request.POST['flujo'])

        flujo.activo = False

        flujo.save()

        return render(request, self.template_name, diccionario)

