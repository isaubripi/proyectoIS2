from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Proyecto
from adm_usuarios.models import Usuario
from adm_roles.models import Rol
from sistemask.views import LoginView

from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import auth

class ProyectoView(TemplateView):
    template_name = 'Proyecto.html'
    context_object_name = 'lista_proyectos'
    def post(self, request, *args, **kwargs):
        diccionario= {}                                                  #Diccionario para ser retornado en HTML
        #Login.html es la unica pagina que envia un 'user' en el diccionario de request.POST
        if 'user' in request.POST:
            existe= Usuario.objects.filter(username=request.POST['user'])
            if len(existe):
                if existe[0].password == request.POST['pass']:
                    diccionario[self.context_object_name]= Proyecto.objects.filter(activo= True)
                    diccionario['logueado']= existe[0]
                    return render(request, self.template_name, diccionario)
                else: error= 'Password incorrecto'
            else: error= 'Nombre de usuario no existe'
            diccionario['error']= error
            return render(request, LoginView.template_name, diccionario)
        else:
            diccionario[self.context_object_name]= Proyecto.objects.filter(activo= True)
            diccionario['logueado']= Usuario.objects.get(id=request.POST['login'])
            return render(request, self.template_name, diccionario)
    def get(self, request, *args, **kwargs):
        return render(request, LoginView.template_name, {'error':'Acceso Incorrecto'})


class CrearProyecto(ProyectoView):
    template_name = 'CrearProyecto.html'
    context_object_name = 'lista_proyectos'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        diccionario[self.context_object_name]= Proyecto.objects.filter(activo= True)
        if len(Rol.objects.filter(nombre= 'Scrum Master', usuario= usuario_logueado)): #Si el logueado es Admin?
            diccionario['lista_usuarios']= Usuario.objects.filter(estado= True)
            del diccionario[self.context_object_name]
            return render(request, self.template_name, diccionario)
        else:
            diccionario['error']= 'No puedes realizar esta accion'
            return render(request, super(CrearProyecto, self).template_name, diccionario)

class CrearProyectoConfirm(CrearProyecto):
    template_name = 'CrearProyectoConfirm.html'
    def post(self, request, *args, **kwargs):
        diccionario= {}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        new_nombre= request.POST['nombre_proyecto']
        existe= Proyecto.objects.filter(nombre= new_nombre)
        if existe:
            diccionario['lista_usuarios']= Usuario.objects.filter(estado= True)
            diccionario['error']= 'Nombre de proyecto ya existe'
            return render(request, super(CrearProyectoConfirm, self).template_name, diccionario)
        else:
            #Creamos el proyecto
            nuevo_proyecto= Proyecto()
            nuevo_proyecto.nombre= new_nombre
            nuevo_proyecto.descripcion= request.POST['descripcion_proyecto']
            new_scrum_master= Usuario.objects.get(username= request.POST['scrum_master'])
            nuevo_proyecto.scrum_master= new_scrum_master
            nuevo_proyecto.save()
            #Agregamos al scrum master a el scrum_team para que pueda visualizar el proyecto
            nuevo_proyecto.scrum_team.add(new_scrum_master)
            nuevo_proyecto.save()
            return render(request, self.template_name, diccionario)

#Eliminacion Logica de Proyectos
class EliminarProyecto(ProyectoView):
    template_name = 'EliminarProyecto.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario[self.context_object_name]= Proyecto.objects.filter(activo= True)
        if len(Rol.objects.filter(nombre= 'Scrum Master', usuario= usuario_logueado, activo= True)):
            if proyecto_actual.estado=='F':
                proyecto_actual.activo= False
                proyecto_actual.save()
                rol_asociado= Rol.objects.get(nombre= 'Scrum Master', usuario= proyecto_actual.scrum_master, activo= True)
                rol_asociado.activo= False
                rol_asociado.save()
                del diccionario[self.context_object_name]  #No hace falta enviar la lista de proyectos
                return render(request, self.template_name, diccionario)
            else:
                diccionario['error']= 'Proyecto No Finalizado - No se puede eliminar'
        else:
            diccionario['error']= 'No puedes realizar esta accion'
        return render(request, super(EliminarProyecto,self).template_name, diccionario)


#Generacion de Informe del Proyecto
class InformeProyecto(ProyectoView):
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario[self.context_object_name]= Proyecto.objects.filter(activo= True)
        if not proyecto_actual.estado == 'N':
            diccionario['proyecto']= proyecto_actual
            del diccionario[self.context_object_name]
            return render(request, 'InformeProyecto.html', diccionario)
        diccionario['error']= 'No se puede mostrar proyecto - No Iniciado'
        return render(request, self.template_name, diccionario)


#Iniciando Proyecto
class InicializarProyecto(ProyectoView):
    template_name = 'InicializarProyecto.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario[self.context_object_name]= Proyecto.objects.filter(activo= True)
        if len(Rol.objects.filter(nombre= 'Scrum Master', usuario= usuario_logueado)):
            if proyecto_actual.estado == 'N':
                diccionario['lista_usuarios']= Usuario.objects.filter(estado= True)
                diccionario['proyecto']= proyecto_actual
                del diccionario[self.context_object_name]
                return render(request, self.template_name, diccionario)
            else:
                diccionario['error']= 'El proyecto ya esta inicializado'
        else:
            diccionario['error']= 'No puede realizar esta accion'
        return render(request, super(InicializarProyecto, self).template_name, diccionario)

class InicializarProyectoConfirm(InicializarProyecto):
    template_name = 'InicializarProyectoConfirm.html'
    def post(self, request, *args, **kwargs):
        diccionario= {}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        proyecto_detalles= Proyecto.objects.get(id= request.POST['proyecto'])
        proyecto_detalles.fecha_inicio= request.POST['fechaInicio']
        proyecto_detalles.fecha_fin= request.POST['fechaFin']
        if proyecto_detalles.fecha_fin < proyecto_detalles.fecha_inicio:
            diccionario['proyecto']= proyecto_detalles
            diccionario['lista_usuarios']= Usuario.objects.filter(estado= True)
            diccionario['error']= 'ERROR - Fecha Inicio posterior a Fecha Fin'
            return render(request, super(InicializarProyectoConfirm, self).template_name, diccionario)
        #proyecto_detalles.sprints= request.POST['sprints']
        usuarios_miembros= request.POST.getlist('miembros[]')
        for i in usuarios_miembros: proyecto_detalles.scrum_team.add(Usuario.objects.get(username= i))
        proyecto_detalles.estado= 'I'
        proyecto_detalles.save()
        proyecto_detalles= Proyecto.objects.get(nombre= proyecto_detalles.nombre)

        return render(request, self.template_name, diccionario)

class Ingresar(TemplateView):
    template_name = 'InicioProyecto.html'
    def post(self, request, *args, **kwargs):
        diccionario = {}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        proyecto_detalles= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['proyecto']= proyecto_detalles
        return render(request,self.template_name, diccionario)

class ModificarProyecto(ProyectoView):
    template_name = 'ModificarProyecto.html'
    context_object_name = 'lista_proyectos'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario[self.context_object_name]= Proyecto.objects.filter(activo= True)
        if len(Rol.objects.filter(nombre= 'Scrum Master', usuario= usuario_logueado)): #Si el logueado es Admin?
            diccionario['lista_usuarios']= Usuario.objects.filter(estado= True)
            del diccionario[self.context_object_name]
            return render(request, self.template_name, diccionario)
        else:
            diccionario['error']= 'No puedes realizar esta accion'
            return render(request, super(ModificarProyecto, self).template_name, diccionario)

class ModificarProyectoConfirm(ModificarProyecto):
    template_name = 'ModificarProyectoConfirm.html'
    def post(self, request, *args, **kwargs):
        diccionario= {}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado

        modificacion= Proyecto.objects.get(id= request.POST['proyecto'])
        modificacion_nombre= request.POST['nombre_proyecto']

        existe= Proyecto.objects.filter(nombre= modificacion_nombre)
        if existe:
            diccionario['lista_usuarios']= Usuario.objects.filter(estado= True)
            diccionario['error']= 'Nombre de proyecto ya existe'
            return render(request, super(ModificarProyectoConfirm, self).template_name, diccionario)
        else:
            #Modificamos  el proyecto
            modificacion.nombre= modificacion_nombre
            modificacion.descripcion= request.POST['descripcion_proyecto']
            new_scrum_master= Usuario.objects.get(username= request.POST['scrum_master'])
            modificacion.scrum_master= new_scrum_master
            modificacion.save()
            #Agregamos al scrum master a el scrum_team para que pueda visualizar el proyecto
            modificacion.scrum_team.add(new_scrum_master)

            modificacion.save()
            return render(request, self.template_name, diccionario)

