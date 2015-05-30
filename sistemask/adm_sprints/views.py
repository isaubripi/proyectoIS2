from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Proyecto
from adm_usuarios.models import Usuario
from adm_roles.models import Rol
from sistemask.views import LoginView
from adm_sprints.models import Sprint
from adm_historias.models import Historia, Registro
from adm_flujos.models import Flujo
from adm_sprints.models import Equipo

from adm_proyectos.views import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from datetime import datetime, date, time, timedelta
import calendar

import matplotlib.pyplot as plt
import numpy as np
from pylab import *


import datetime
class SprintView(TemplateView):

    template_name = 'Sprint.html'
    context_object_name = 'lista_sprints'

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """

        :param request: Peticion Web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return:Pagina de inicio de Adm sprints.
        """

        diccionario= {}
        #obtiene el proyecto actual
        proyecto_actual = Proyecto.objects.get(id = request.POST['proyecto'])
        diccionario[self.context_object_name]= Sprint.objects.filter(activo= True, proyecto= proyecto_actual)


        diccionario['logueado']= Usuario.objects.get(id=request.POST['login'])
        proyecto_detalles= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['proyecto']= proyecto_detalles
        return render(request, self.template_name, diccionario)



class CrearSprint(LoginRequiredMixin, SprintView):
    """
    Esta clase es la engarcada de crear un sprint
    Hereda de la clase SprintView
    """
    template_name = 'CrearSprint.html'
    context_object_name = 'lista_sprints'
    def post(self, request, *args, **kwargs):
        """
        Se encarga de crear un nuevo sprint, teniendo como condicion que el usuario sea SM
        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: Retorna el formulacion para creacion de sprint solo si el usuario posee el rol de Scrum Master
                 En caso contrario retorna un mensaje de denegacion de acceso en la misma pagina.
        """
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual = Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        diccionario[self.context_object_name]= Sprint.objects.filter(activo= True, proyecto = proyecto_actual)
        if len(Rol.objects.filter(agregar_sprint=True, usuario= usuario_logueado)): #Si el logueado es Scrum Master
            #diccionario['lista_usuarios']= Usuario.objects.filter(estado= True)
            #del diccionario[self.context_object_name]
            return render(request, self.template_name, diccionario)
        else:
            diccionario['error']= 'No posee permiso para crear sprint'
            return render(request, super(CrearSprint, self).template_name, diccionario)

class CrearSprintConfirm(CrearSprint):
    """
    Para confirmar una creacion de sprint. Boton "Guardar"
    """
    template_name = 'CrearSprintConfirm.html'
    def post(self, request, *args, **kwargs):
        """
        Se encarga de verificar que el  nombre del proyecto no se repita
        para luego crear exitosamente el mismo

        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: Retorna un mensaje de error (en el caso que el nombre de sprint ya exista) en la misma pagina
                 Retorna una pagina en donde se muestra la creacion existosa del sprint.
        """

        diccionario= {}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual = Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        new_nombre= request.POST['nombre_sprint']
        existe= Sprint.objects.filter(nombre= new_nombre)
        if existe:
            diccionario['lista_usuarios']= Usuario.objects.filter(estado= True)
            diccionario['error']= 'Nombre de sprint ya existe'
            return render(request, super(CrearSprintConfirm, self).template_name, diccionario)
        else:
            #Creamos el sprint
            nuevo_sprint= Sprint()
            nuevo_sprint.nombre= new_nombre
            nuevo_sprint.descripcion= request.POST['descripcion_sprint']
            nuevo_sprint.fecha_inicio = request.POST['fecha_inicio']
            nuevo_sprint.fecha_fin = request.POST['fecha_fin']
            if nuevo_sprint.fecha_fin < nuevo_sprint.fecha_inicio:
                diccionario['error']= 'ERROR - Fecha Inicio posterior a Fecha Fin'
                return render(request, super(CrearSprintConfirm, self).template_name, diccionario)
            #if nuevo_sprint.fecha_fin > proyecto_actual.fecha_fin and nuevo_sprint.fecha_inicio < proyecto_actual.fecha_inicio:
             #   diccionario['error']= 'ERROR - Las Fechas de inicio y fin deben contenerse dentro de la duracion del Proyecto'
            #  return render(request, super(CrearSprintConfirm, self).template_name, diccionario)

            nuevo_sprint.duracion = request.POST['duracion']
            new_proyecto= Proyecto.objects.get(id= request.POST['proyecto'])
            nuevo_sprint.proyecto= new_proyecto
            nuevo_sprint.save()
            diccionario['sprint']=nuevo_sprint
            return render(request, self.template_name, diccionario)

class EliminarSprint(LoginRequiredMixin, SprintView):
    """
    Para eliminar un sprint en forma logica. Boton "Eliminar"
    """
    template_name = 'EliminarSprint.html'
    def post(self, request, *args, **kwargs):
        """
        Realiza la verificacion de roles,
        luego elimina si es posible.

        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: Retorna la pagina de eliminacion exitosa del sprint (paso de activo a inactivo)
                 Retorna mensajes de error en caso de que el usuario no sea SM.
        """
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        sprint_actual = Sprint.objects.get(id =request.POST['sprint'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        diccionario[self.context_object_name]= Sprint.objects.filter(activo= True, proyecto= proyecto_actual)

        if len(Rol.objects.filter(eliminar_sprint=True, usuario= usuario_logueado, activo= True)):
            if sprint_actual.estado=='Futuro' and sprint_actual.asignado_h == False:
                sprint_actual.activo= False
                sprint_actual.save()
                del diccionario[self.context_object_name]  #No hace falta enviar la lista de proyectos
                return render(request, self.template_name, diccionario)
            else:
                diccionario['error']= 'Sprint en Ejecucion, Ejecutado o con Historias de Usuario asignadas- No se puede eliminar'
        else:
            diccionario['error']= 'No posee permiso para eliminar sprint'
        return render(request, super(EliminarSprint,self).template_name, diccionario)


class ModificarSprint(LoginRequiredMixin, SprintView):
    """
    Modificacion de los campos del formulario sprint
    """
    template_name = 'ModificarSprint.html'
    context_object_name = 'lista_sprints'
    def post(self, request, *args, **kwargs):
        """

        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: Retorna la pagina de modificacion , con  los datos pre-cargados
                 Retorna un mensaje de error, si el usuario no posee el rol correspondiente
        """
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= Proyecto.objects.get(id= request.POST['proyecto'])
        sprint_actual = Sprint.objects.get(id =request.POST['sprint'])
        diccionario['sprint'] = sprint_actual

        proyecto_actual = Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario[self.context_object_name]= Sprint.objects.filter(activo= True, proyecto= proyecto_actual)

        if len(Rol.objects.filter(modificar_sprint=True, usuario= usuario_logueado)): #Si el logueado es SM
            diccionario['lista_usuarios']= Usuario.objects.filter(estado= True)
            diccionario[self.context_object_name]
            if sprint_actual.estado == 'Futuro':
                return render(request, self.template_name, diccionario)
            else:
                diccionario['error']= 'Sprint En Ejecucion o Ejecutado, no se puede modificar'
                return render(request, super(ModificarSprint, self).template_name, diccionario)
        else:
            diccionario['error']= 'No posee permiso para modificar sprint'
            return render(request, super(ModificarSprint, self).template_name, diccionario)

class ModificarSprintConfirm(ModificarSprint):
    """
    Confirma la modificacion de un sprint
    """
    template_name = 'ModificarSprintConfirm.html'
    def post(self, request, *args, **kwargs):
        """
        Realiza la verificacion de que el nombre del sprint sea unico y luego actualiza los datos.

        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: Retorna un mensaje de error, en el caso de que el nombre del sprint sea repetido.
                Retorna la pagina de modificacion exitosa del sprint
        """
        diccionario= {}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado

        diccionario['proyecto']= Proyecto.objects.get(id= request.POST['proyecto'])

        modificacion= Sprint.objects.get(id= request.POST['sprint'])
        modificacion_nombre= request.POST['nombre_sprint']

        existe= Sprint.objects.filter(nombre= modificacion_nombre, activo=True)
        if len(existe) and existe[0]!=modificacion:
            diccionario['lista_usuarios']= Usuario.objects.filter(estado= True)
            diccionario['error']= 'Nombre de sprint ya existe'
            return render(request, super(ModificarSprintConfirm, self).template_name, diccionario)
        else:
            #Modificamos  el sprint
            modificacion.nombre= modificacion_nombre
            modificacion.descripcion= request.POST['descripcion_sprint']
            modificacion.fecha_inicio = request.POST['fecha_inicio']
            modificacion.fecha_fin = request.POST['fecha_fin']
            modificacion.duracion = request.POST['duracion']
            modificacion.save()

            return render(request, self.template_name, diccionario)

class CambiarEstado(LoginRequiredMixin, SprintView):
    """
    Establecer el estado de un sprint, en 3 posibles: Futuro, En ejecucion, Ejecutado
    """

    template_name = 'CambiarEstado.html'
    def post(self, request, *args, **kwargs):
        """

        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: Retorna un mensaje de exito si el estado es cambiado
                Retorna un mensaje de error en el caso que el usuario no pueda cambiar de estado
        """

        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado

        diccionario['proyecto']= Proyecto.objects.get(id= request.POST['proyecto'])
        sprint_actual = Sprint.objects.get(id= request.POST['sprint'])

        proyecto_actual = Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario[self.context_object_name]= Sprint.objects.filter(activo= True, proyecto= proyecto_actual)

        sprint_actual = Sprint.objects.get(id=request.POST['sprint'])
        diccionario['sprint']=sprint_actual
        if len(Rol.objects.filter(activar_sprint=True, usuario= usuario_logueado)):

            return render(request, self.template_name, diccionario)

        else:
            diccionario['error'] = 'No posee permiso para cambiar estado'
            return render(request, super(CambiarEstado, self).template_name, diccionario)



class CambiarEstadoConfirm(CambiarEstado):
    """
    pasar un sprint del estado P(Planeado) al estado A(Activo)
    """

    template_name = 'CambiarEstadoConfirm.html'
    def post(self, request, *args, **kwargs):
        """

        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: Retorna un mensaje de exito en donde cambia el estado de P a A
                Retorna un mensaje de error en el caso que el usuario no pueda activar un sprint
        """

        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado

        diccionario['proyecto']= Proyecto.objects.get(id= request.POST['proyecto'])


        proyecto_actual = Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario[self.context_object_name]= Sprint.objects.filter(activo= True, proyecto= proyecto_actual)

        sprint_actual = Sprint.objects.get(id=request.POST['sprint'])
        diccionario['sprint']=sprint_actual

        estado_actual = request.POST['estado_sprint']
        id_sprint = request.POST['sprint']

        if len(Rol.objects.filter(activar_sprint=True, usuario= usuario_logueado)):
            #si el estado ya se encuentra en futuro y se asigna nuevamente futuro, no pasa nada
            if estado_actual == 'Futuro' and sprint_actual.estado=='Futuro':
                sprint_actual.estado = 'Futuro'
                sprint_actual.save()
            #si se quiere establecer En ejecucion, posee historias pero ya se encuentra otro en ejecucion
            elif estado_actual == 'En Ejecucion' and sprint_actual.asignado_h==True and Sprint.objects.filter(activo=True, proyecto=proyecto_actual, estado='En Ejecucion' ):
                diccionario['error'] = 'El Sprint no se puede ejecutar, ya que otro Sprint se encuentra en Ejecucion'
                return render(request, super(CambiarEstadoConfirm, self).template_name, diccionario)

            elif estado_actual == 'Ejecutado' and sprint_actual.estado=='En Ejecucion' and not len(Historia.objects.filter(proyecto=proyecto_actual, sprint=id_sprint, activo=True, estado_sprint='Completada').all()):
                sprint_actual.estado = 'Ejecutado'
                sprint_actual.save()

            elif estado_actual == 'Ejecutado' and sprint_actual.estado=='En Ejecucion' and len(Historia.objects.filter(proyecto=proyecto_actual, sprint=id_sprint, activo=True, estado_sprint='Completada').all()):
                diccionario['error'] = 'El Sprint no se puede finalizar, quedan historias no completadas'
                return render(request, super(CambiarEstadoConfirm, self).template_name, diccionario)

            #si se quiere establer En ejecucion, posee historias y no hay otro en ejecucion
            elif estado_actual == 'En Ejecucion' \
                    and sprint_actual.asignado_h==True \
                    and not Sprint.objects.filter(activo=True, proyecto=proyecto_actual, estado='En Ejecucion' ) \
                    and len(Historia.objects.filter(proyecto=proyecto_actual, sprint=id_sprint, activo=True))\
                    and len(Equipo.objects.filter(sprint=id_sprint))\
                    and len(Historia.objects.filter(proyecto=proyecto_actual, sprint=id_sprint, activo=True, asignado = Usuario.objects.all(), flujo=Flujo.objects.all())):
                    sprint_actual.estado = 'En Ejecucion'

                    historias = Historia.objects.filter(proyecto=proyecto_actual, sprint=id_sprint, activo=True)
                    for i in historias:
                        i.estado_sprint = 'En Progreso'
                        i.save()

                    sprint_actual.save()
            elif estado_actual== 'En Ejecucion'\
                    or not len(Historia.objects.filter(proyecto=proyecto_actual, sprint=id_sprint, activo=True))\
                    or not len(Equipo.objects.filter(sprint=id_sprint))\
                    or not len(Historia.objects.filter(proyecto=proyecto_actual, sprint=id_sprint, activo=True, asignado = Usuario.objects.all(), flujo=Flujo.objects.all())):
                diccionario['error']='El sprint no se puede iniciar, ya que no posee historias asignadas inicializadas o equipo asignado'
                return render(request, super(CambiarEstadoConfirm, self).template_name, diccionario)



            return render(request, self.template_name, diccionario)

        else:
            diccionario['error'] = 'No puedes realizar esta accion'
            return render(request, super(CambiarEstadoConfirm, self).template_name, diccionario)



class AsignarHistorias(LoginRequiredMixin, SprintView):
    """
    Permite asignar historias de usuario a un sprint
    """

    template_name = 'AsignarHistorias.html'
    context_object_name = 'lista_sprints'
    def post(self, request, *args, **kwargs):
        """

        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: Retorna la interfaz de asignacion de historias de usuario, si posee el rol
                Retorna un mensaje de error en el caso que el usuario no pueda asignar historias a un sprint
        """

        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado

        diccionario['proyecto']= Proyecto.objects.get(id= request.POST['proyecto'])

        proyecto_actual = Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario[self.context_object_name]= Sprint.objects.filter(activo= True, proyecto= proyecto_actual)
        diccionario['historias']= Historia.objects.filter(activo= True, proyecto= proyecto_actual, asignado_p = False)

        sprint_actual = Sprint.objects.get(id = request.POST['sprint'])
        diccionario['sprint']=sprint_actual


        if len(Rol.objects.filter(asignar_historia=True, usuario= usuario_logueado)):
            if sprint_actual.estado=='Futuro':
                return render(request, self.template_name, diccionario)
            else:
                diccionario['error'] = 'El Sprint se encuenta En ejecucion o Ejecutado, ya no se pueden asignar historias'
                return render(request, super(AsignarHistorias, self).template_name, diccionario)

        else:
             diccionario['error'] = 'No puedes realizar esta accion'
             return render(request, super(AsignarHistorias, self).template_name, diccionario)


class AsignarHistoriasConfirm(AsignarHistorias):
    """
    Confirma la asignacion de historias a un sprint especifico
    """

    template_name = 'AsignarHistoriasConfirm.html'
    context_object_name = 'lista_sprints'

    def post(self, request, *args, **kwargs):
        """

        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: Retorna la interfaz de exito para la asignacion de historias

        """

        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado

        diccionario['proyecto']= Proyecto.objects.get(id= request.POST['proyecto'])

        proyecto_actual = Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario[self.context_object_name]= Sprint.objects.filter(activo= True, proyecto= proyecto_actual)
        diccionario['historias']= Historia.objects.filter(activo= True, proyecto= proyecto_actual)

        sprint_actual = Sprint.objects.get(id = request.POST['sprint'])
        diccionario['sprint']=sprint_actual

        sprint_detalles = Sprint.objects.get(id=request.POST['sprint'])
        sprint_detalles.asignado_h = True
        stories = request.POST.getlist('historias[]')

        id_sprint = request.POST['sprint']

        for i in stories:

            H = Historia.objects.get(nombre=i)

            if H.asignado_p == False:

                sprint_detalles.historias.add(Historia.objects.get(nombre=i))
                Historia_asignada = Historia.objects.get(nombre=i)
                Historia_asignada.sprint = id_sprint
                Historia_asignada.asignado_p = True
                Historia_asignada.estado_sprint = 'No iniciado'
                Historia_asignada.horas_sprint = 0
                Historia_asignada.save()
            else:
                diccionario['error']= 'Una de las historias no tiene asignados Usuario y Flujo, no se puede agregar al Sprint'
                return render(request, super(AsignarHistoriasConfirm, self).template_name, diccionario)


        sprint_detalles.save()

        return render(request, self.template_name, diccionario)


class AsignarUsuarioFlujo(LoginRequiredMixin, SprintView):

    template_name = 'AsignarUsuarioFlujo.html'
    context_object_name = 'lista_sprints'
    def post(self, request, *args, **kwargs):
        """

        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: Retorna la interfaz de asignacion de historias de usuario, si posee el rol
                Retorna un mensaje de error en el caso que el usuario no pueda asignar historias a un sprint
        """

        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado

        diccionario['proyecto']= Proyecto.objects.get(id= request.POST['proyecto'])

        proyecto_actual = Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario[self.context_object_name]= Sprint.objects.filter(activo= True, proyecto= proyecto_actual)
        diccionario['historias']= Historia.objects.filter(activo= True, proyecto= proyecto_actual, sprint=request.POST['sprint'])

        sprint_actual = Sprint.objects.get(id = request.POST['sprint'])
        diccionario['sprint']=sprint_actual

        diccionario['lista_flujos'] = Flujo.objects.filter(activo= True, proyecto=proyecto_actual)

        if len(Rol.objects.filter(asignar_usuario_flujo = True, usuario= usuario_logueado)):
            if sprint_actual.estado == 'Futuro':
                if len(Equipo.objects.filter(sprint = request.POST['sprint'])):
                    return render(request, self.template_name, diccionario)
                else:
                    diccionario['error']='Primero debe asignar el Equipo de Trabajo'
                    return render(request, super(AsignarUsuarioFlujo, self).template_name, diccionario)
            else:
                diccionario['error']='Sprint En Ejecucion o Ejecutado, ya no se pueden asignar Usuario y Flujo'
                return render(request, super(AsignarUsuarioFlujo, self).template_name, diccionario)
        else:
             diccionario['error'] = 'No puedes realizar esta accion'
             return render(request, super(AsignarUsuarioFlujo, self).template_name, diccionario)

class AsignarUsuarioFlujo1(AsignarHistorias):

    template_name = 'AsignarUsuarioFlujo1.html'
    context_object_name = 'lista_sprints'
    def post(self, request, *args, **kwargs):
        """

        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: Retorna la interfaz de asignacion de historias de usuario, si posee el rol
                Retorna un mensaje de error en el caso que el usuario no pueda asignar historias a un sprint
        """

        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado

        diccionario['proyecto']= Proyecto.objects.get(id= request.POST['proyecto'])


        proyecto_actual = Proyecto.objects.get(id= request.POST['proyecto'])

        Historia_actual = Historia.objects.get(id = request.POST['historia'])

        diccionario['historia'] = Historia_actual
        diccionario[self.context_object_name]= Sprint.objects.filter(activo= True, proyecto= proyecto_actual)
        diccionario['historias']= Historia.objects.filter(activo= True, proyecto= proyecto_actual)

        sprint_actual = Sprint.objects.get(id = request.POST['sprint'])
        diccionario['sprint']=sprint_actual

        diccionario['lista_usuarios'] = Usuario.objects.filter(estado = True)

        diccionario['lista_flujos'] = Flujo.objects.filter(activo= True, proyecto=proyecto_actual)

        if len(Rol.objects.filter(asignar_usuario_flujo = True , usuario= usuario_logueado)):
             return render(request, self.template_name, diccionario)

        else:
             diccionario['error'] = 'No puedes realizar esta accion'
             return render(request, super(AsignarUsuarioFlujo1, self).template_name, diccionario)


class AsignarUsuarioFlujo2(AsignarUsuarioFlujo1):

    template_name = 'AsignarUsuarioFlujoConfirm.html'

    def post(self, request, *args, **kwargs):
        """

        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: Retorna la interfaz de asignacion de historias de usuario, si posee el rol
                Retorna un mensaje de error en el caso que el usuario no pueda asignar historias a un sprint
        """

        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado

        diccionario['proyecto']= Proyecto.objects.get(id= request.POST['proyecto'])


        proyecto_actual = Proyecto.objects.get(id= request.POST['proyecto'])

        Historia_actual = Historia.objects.get(id = request.POST['historia'])

        diccionario['historia'] = Historia_actual
        diccionario[self.context_object_name]= Sprint.objects.filter(activo= True, proyecto= proyecto_actual)
        diccionario['historias']= Historia.objects.filter(activo= True, proyecto= proyecto_actual)

        sprint_actual = Sprint.objects.get(id = request.POST['sprint'])
        diccionario['sprint']=sprint_actual


        diccionario['lista_flujos'] = Flujo.objects.filter(activo= True)


        if len(Rol.objects.filter(asignar_usuario_flujo = True, usuario= usuario_logueado)):
            Usuario_asignado = Usuario.objects.get(username = request.POST['usuario'])
            Flujo_asignado = Flujo.objects.get(nombre = request.POST['flujo'])

            Historia_actual.asignado = Usuario_asignado
            Historia_actual.flujo = Flujo_asignado
            Historia_actual.save()

            return render(request, self.template_name, diccionario)

        else:
             diccionario['error'] = 'No puedes realizar esta accion'
             return render(request, super(AsignarUsuarioFlujo2, self).template_name, diccionario)

class DesasignarHistorias(LoginRequiredMixin, SprintView):
    """
    Permite desasignar historias de usuario a un sprint
    """

    template_name = 'DesasignarHistorias.html'
    context_object_name = 'lista_sprints'
    def post(self, request, *args, **kwargs):
        """

        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: Retorna la interfaz de asignacion de historias de usuario, si posee el rol
                Retorna un mensaje de error en el caso que el usuario no pueda desasignar historias de un sprint

                Esta funcion es la encargada de presentar al usuario aquellas historias de usuario
                que ya fueron asignadas con anterioridad, dandole la posibilidad de que el mismo
                pueda elegir aquellas historias que ya no perteneceran al sprint actual.
        """

        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado

        diccionario['proyecto']= Proyecto.objects.get(id= request.POST['proyecto'])


        id_sprint = request.POST['sprint']
        proyecto_actual = Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario[self.context_object_name]= Sprint.objects.filter(activo= True, proyecto= proyecto_actual)
        diccionario['historias']= Historia.objects.filter(activo= True, proyecto= proyecto_actual, asignado_p = True, sprint=id_sprint)

        sprint_actual = Sprint.objects.get(id = request.POST['sprint'])
        diccionario['sprint']=sprint_actual

        equipo_scrum = proyecto_actual.scrum_team
        diccionario['lista_usuarios'] = Usuario.objects.filter(estado = True)

        diccionario['lista_flujos'] = Flujo.objects.filter(activo= True)

        if len(Rol.objects.filter(desasignar_historia = True, usuario= usuario_logueado)):
            if sprint_actual.estado == 'Futuro':
                return render(request, self.template_name, diccionario)
            else:
                diccionario['error'] = 'Sprint En Ejecucion o Ejecutado, no se pueden desasignar Historias'
                return render(request, super(DesasignarHistorias, self).template_name, diccionario)

        else:
             diccionario['error'] = 'No puedes realizar esta accion'
             return render(request, super(DesasignarHistorias, self).template_name, diccionario)


class DesasignarHistoriasConfirm(DesasignarHistorias):
    """
    Confirma la asignacion de historias a un sprint especifico
    """

    template_name = 'AsignarHistoriasConfirm.html'
    context_object_name = 'lista_sprints'

    def post(self, request, *args, **kwargs):
        """

        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: Retorna la interfaz de exito para la desasignacion de historias


        Se quitan de la lista del sprint, aquellas historias de usuario que se desean
        agreagar en algun otro sprint.
        """

        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado

        diccionario['proyecto']= Proyecto.objects.get(id= request.POST['proyecto'])

        proyecto_actual = Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario[self.context_object_name]= Sprint.objects.filter(activo= True, proyecto= proyecto_actual)
        diccionario['historias']= Historia.objects.filter(activo= True, proyecto= proyecto_actual)

        sprint_actual = Sprint.objects.get(id = request.POST['sprint'])
        diccionario['sprint']=sprint_actual

        sprint_detalles = Sprint.objects.get(id=request.POST['sprint'])
        sprint_detalles.asignado_h = True
        stories = request.POST.getlist('historias[]')

        id_sprint = request.POST['sprint']

        for i in stories:

            H = Historia.objects.get(nombre=i)

            if H.asignado_p == True:

                sprint_detalles.historias.remove(Historia.objects.get(nombre=i))
                Historia_desasignada = Historia.objects.get(nombre=i)
                Historia_desasignada.sprint = ''
                Historia_desasignada.asignado_p = False
                Historia_desasignada.asignado = None
                Historia_desasignada.flujo = None
                Historia_desasignada.save()
            else:
                diccionario['error']= 'Una de las historias no tiene asignados Usuario y Flujo, no se puede agregar al Sprint'
                return render(request, super(AsignarHistoriasConfirm, self).template_name, diccionario)


        sprint_detalles.save()

        return render(request, self.template_name, diccionario)

class VerInformacionSprint(LoginRequiredMixin, SprintView):

    template_name = 'VerInformacionSprint.html'
    context_object_name = 'lista_sprints'

    def post(self, request, *args, **kwargs):
        """

        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: Retorna un informe con todos los datos del sprint


        Esta funcion muestra todos los datos relacionados a un sprint en particular

        """

        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado

        diccionario['proyecto']= Proyecto.objects.get(id= request.POST['proyecto'])

        proyecto_actual = Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario[self.context_object_name]= Sprint.objects.filter(activo= True, proyecto= proyecto_actual)

        id_sprint = request.POST['sprint']
        sprint_actual = Sprint.objects.get(id = request.POST['sprint'])
        diccionario['sprint']=sprint_actual

        Historias_sprint = Historia.objects.filter(proyecto=proyecto_actual, sprint=id_sprint, activo=True)
        diccionario['historias_sprint']=Historias_sprint

        usuarios_sprint = []

        '''for i in Historias_sprint:
            nombre = i.asignado
            usuarios_sprint.append(nombre.username)

        usuarios_sprint=list(set(usuarios_sprint))'''

        #calcular la capacidad productiva en base a las horas asignadas a cada usuario
        #primero se calculan la horas que puede trabajar un equipo por dia
        horas_dia = 0
        for i in sprint_actual.equipo.all():
            horas_dia = horas_dia + i.horas_sprint
            usuarios_sprint.append(i)


        #elementos = len(usuarios_sprint)
        capacidad_productiva = horas_dia*(sprint_actual.duracion)

        # calcular cantidad de horas que requiere el sprint (suma de todas las horas estimadas)
        horas = 0
        for j in sprint_actual.historias.all():
            horas = horas + j.size

        horas_trabajadas=0
        for k in sprint_actual.historias.all():
            horas_trabajadas = horas_trabajadas + k.acumulador

        #se calcula el saldo en horas de trabajo
        saldo=0
        saldo = horas - horas_trabajadas

        diccionario['saldo']=saldo
        diccionario['horas_trabajo']=horas

        diccionario['capacidad'] = capacidad_productiva
        diccionario['usuarios']=usuarios_sprint


        if len(Rol.objects.filter(usuario= usuario_logueado)):
             return render(request, self.template_name, diccionario)

        else:
             diccionario['error'] = 'No puedes realizar esta accion'
             return render(request, super(VerInformacionSprint, self).template_name, diccionario)

class AsignarEquipo(LoginRequiredMixin, SprintView):
    """
    Permite asignar aquellos usuarios que trabajaran en el sprint
    """

    template_name = 'AsignarEquipo.html'
    context_object_name = 'lista_sprints'
    def post(self, request, *args, **kwargs):
        """

        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: Retorna la interfaz de asignacion de equipo, si posee el rol
                Retorna un mensaje de error en el caso que el usuario no pueda asignar usuarios a un sprint
        """

        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado

        diccionario['proyecto']= Proyecto.objects.get(id= request.POST['proyecto'])

        proyecto_actual = Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario[self.context_object_name]= Sprint.objects.filter(activo= True, proyecto= proyecto_actual)
        #diccionario['historias']= Historia.objects.filter(activo= True, proyecto= proyecto_actual, asignado_p = False, asignado = Usuario.objects.all, flujo=Flujo.objects.all)

        #diccionario['usuarios_proyecto']=
        sprint_actual = Sprint.objects.get(id = request.POST['sprint'])
        diccionario['sprint']=sprint_actual

        equipo_scrum = proyecto_actual.scrum_team
        diccionario['lista_usuarios'] = Usuario.objects.filter(estado = True)

        diccionario['lista_flujos'] = Flujo.objects.filter(activo= True)

        if len(Rol.objects.filter(asignar_equipo = True, usuario= usuario_logueado)):
            if sprint_actual.estado == 'Futuro':
                return render(request, self.template_name, diccionario)
            else:
                diccionario['error'] = 'Sprint En Ejecucion o Ejecutado, no se puede asignar Equipo de Trabajo'
                return render(request, super(AsignarEquipo, self).template_name, diccionario)

        else:
             diccionario['error'] = 'No puedes realizar esta accion'
             return render(request, super(AsignarEquipo, self).template_name, diccionario)


class AsignarEquipoConfirm(AsignarHistorias):
    """
    Confirma la asignacion de usuario a un sprint especifico
    """

    template_name = 'AsignarEquipoConfirm.html'
    context_object_name = 'lista_sprints'

    def post(self, request, *args, **kwargs):
        """

        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: Retorna la interfaz de exito para la asignacion de usuarios a sprint

        """

        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado

        diccionario['proyecto']= Proyecto.objects.get(id= request.POST['proyecto'])

        proyecto_actual = Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario[self.context_object_name]= Sprint.objects.filter(activo= True, proyecto= proyecto_actual)
        diccionario['historias']= Historia.objects.filter(activo= True, proyecto= proyecto_actual)

        sprint_actual = Sprint.objects.get(id = request.POST['sprint'])

        #usuario a agregar al sprint
        for i in sprint_actual.equipo.all():
            if i.usuario == Usuario.objects.get(id=request.POST['usuario']):

                team= Equipo.objects.get(usuario=Usuario.objects.get(id=request.POST['usuario']))
                team.horas_sprint = request.POST['horas']
                team.save()

                diccionario['sprint']=sprint_actual
                return render(request, self.template_name, diccionario)


        team = Equipo()
        team.usuario = Usuario.objects.get(id=request.POST['usuario'])
        team.horas_sprint = request.POST['horas']
        team.save()
        sprint_actual.equipo.add(team)
        sprint_actual.save()

        diccionario['sprint']=sprint_actual

        return render(request, self.template_name, diccionario)

class AsignarHoras(AsignarEquipo):

    template_name = 'AsignarHoras.html'
    context_object_name = 'lista_sprints'
    def post(self, request, *args, **kwargs):
        """

        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: Retorna la interfaz de asignacion de horas a usuario, si posee el rol
                Retorna un mensaje de error en el caso que el usuario no pueda asignar horas a un usuario dentro de un sprint
        """

        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado

        diccionario['proyecto']= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['usuario']=Usuario.objects.get(id=request.POST['user'])

        proyecto_actual = Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario[self.context_object_name]= Sprint.objects.filter(activo= True, proyecto= proyecto_actual)
        diccionario['historias']= Historia.objects.filter(activo= True, proyecto= proyecto_actual)

        sprint_actual = Sprint.objects.get(id = request.POST['sprint'])
        diccionario['sprint']=sprint_actual

        equipo_scrum = []
        equipo_scrum = proyecto_actual.scrum_team
        diccionario['lista_usuarios'] = equipo_scrum

        diccionario['lista_flujos'] = Flujo.objects.filter(activo= True, proyecto=proyecto_actual)

        if len(Rol.objects.filter(asignar_equipo = True , usuario= usuario_logueado)):
             return render(request, self.template_name, diccionario)

        else:
             diccionario['error'] = 'No puedes realizar esta accion'
             return render(request, super(AsignarEquipo, self).template_name, diccionario)

class Sprintbacklog(LoginRequiredMixin, SprintView):

    template_name = 'Sprintbacklog.html'
    context_object_name = 'lista_sprints'
    def post(self, request, *args, **kwargs):
        """

        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: Retorna la vista donde estan todas las historiad de usuarios asignadas al sprint actual
                Retorna un mensaje de error en el caso que el usuario no pueda ver el sprint backlog
        """

        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado

        diccionario['proyecto']= Proyecto.objects.get(id= request.POST['proyecto'])

        proyecto_actual = Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario[self.context_object_name]= Sprint.objects.filter(activo= True, proyecto= proyecto_actual)
        diccionario['historias']= Historia.objects.filter(activo= True, proyecto= proyecto_actual, sprint=request.POST['sprint'])

        sprint_actual = Sprint.objects.get(id = request.POST['sprint'])
        diccionario['sprint']=sprint_actual

        usuarios_sprint = []

        '''for i in Historias_sprint:
            nombre = i.asignado
            usuarios_sprint.append(nombre.username)

        usuarios_sprint=list(set(usuarios_sprint))'''

        #calcular la capacidad productiva en base a las horas asignadas a cada usuario
        #primero se calculan la horas que puede trabajar un equipo por dia
        horas_dia = 0
        for i in sprint_actual.equipo.all():
            horas_dia = horas_dia + i.horas_sprint
            usuarios_sprint.append(i)


        #elementos = len(usuarios_sprint)
        capacidad_productiva = horas_dia*(sprint_actual.duracion)

        # calcular cantidad de horas que requiere el sprint (suma de todas las horas estimadas)
        horas = 0
        for j in sprint_actual.historias.all():
            horas = horas + j.size

        horas_trabajadas=0
        for k in sprint_actual.historias.all():
            horas_trabajadas = horas_trabajadas + k.acumulador

        #se calcula el saldo en horas de trabajo
        saldo=0
        saldo = horas - horas_trabajadas

        diccionario['saldo']=saldo
        diccionario['horas_trabajo']=horas

        diccionario['capacidad'] = capacidad_productiva
        diccionario['usuarios']=usuarios_sprint

        if len(Rol.objects.filter(usuario= usuario_logueado)):
             return render(request, self.template_name, diccionario)

        else:
             diccionario['error'] = 'No puedes realizar esta accion'
             return render(request, super(Sprintbacklog, self).template_name, diccionario)

class BurndownChart(LoginRequiredMixin, SprintView):

    template_name = 'Sprint.html'
    context_object_name = 'lista_sprints'

    def post(self, request, *args, **kwargs):

        """
        Se encarga de crear un nuevo sprint, teniendo como condicion que el usuario sea SM
        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: Retorna el formulacion para creacion de sprint solo si el usuario posee el rol de Scrum Master
                 En caso contrario retorna un mensaje de denegacion de acceso en la misma pagina.
        """
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual = Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        diccionario[self.context_object_name]= Sprint.objects.filter(activo= True, proyecto = proyecto_actual)

        sprint_actual = Sprint.objects.get(id=request.POST['sprint'])

        duracion = sprint_actual.fecha_fin - sprint_actual.fecha_inicio
        inicio = sprint_actual.fecha_inicio


        lista_fechas = []
        for j in range(1, duracion.days):

            lista_fechas.append(inicio)
            inicio = inicio + timedelta(days=1)

        registros = Registro.objects.all()
        lista_horas = []

        for i in lista_fechas:
            horas = 0
            for j in registros:
                if i == j.fecha:
                    horas = horas + j.horas
            lista_horas.append(horas)

        historias_sprint = Historia.objects.filter(sprint=sprint_actual, activo=True)

        horas_estimadas=0
        for i in historias_sprint:
            horas_estimadas = horas_estimadas + i.size



        x = np.array([0,1,2])
        y = np.array([horas_estimadas, 0, 0])

        plt.xlabel('Dias de la iteracion')
        plt.ylabel('Horas restantes del Sprint')




        plt.title('Burndown Chart del '+ sprint_actual.nombre)

        plt.plot(x, y)

        #show plot
        plt.show()

        return render(request, self.template_name, diccionario)

class FinalizarHistoria(LoginRequiredMixin, SprintView):
    template_name = 'FinalizarHistoria.html'

    def post(self, request, *args, **kwargs):

        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual = Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual

        historia_actual = Historia.objects.get(id=request.POST['historia'])
        sprint_actual = Sprint.objects.get(id=request.POST['sprint'])
        diccionario['sprint']=sprint_actual

        if len(Rol.objects.filter(finalizar_historia=True, usuario=usuario_logueado, activo=True)):
            historia_actual.estado_sprint = 'Completada'
            historia_actual.asignado_p = False
            historia_actual.save()
            return render(request, self.template_name, diccionario)
        else:
            diccionario['error']='No posee el permiso para finalizar Historia'
            return render(request, super(FinalizarHistoria, self).template_name, diccionario)

class HorasSprint(LoginRequiredMixin, SprintView):
    template_name = 'HorasSprint.html'

    def post(self, request, *args, **kwargs):

        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual = Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual

        sprint_actual = Sprint.objects.get(id=request.POST['sprint'])
        diccionario['sprint']=sprint_actual

        historia_actual = Historia.objects.get(id=request.POST['historia'])
        diccionario['historia']=historia_actual

        if len(Rol.objects.filter(horas_sprint=True, usuario=usuario_logueado, activo=True)):
            return render(request, self.template_name, diccionario)
        else:
            diccionario['error']='No posee el permiso'
            return render(request, super(HorasSprint, self).template_name, diccionario)

class HorasSprintConfirm(LoginRequiredMixin, SprintView):
    template_name = 'HorasSprintConfirm.html'

    def post(self, request, *args, **kwargs):

        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual = Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual

        sprint_actual = Sprint.objects.get(id=request.POST['sprint'])
        diccionario['sprint']=sprint_actual

        historia_actual = Historia.objects.get(id=request.POST['historia'])
        hs_sprint = request.POST['horas_sprint']

        historia_actual.horas_sprint = hs_sprint
        historia_actual.save()

        return render(request, self.template_name, diccionario)


class Burndownchart(LoginRequiredMixin, SprintView):


    template_name = 'Burndownchart.html'
    def post(self, request, *args, **kwargs):
        '''

        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado

        diccionario['proyecto']= Proyecto.objects.get(id= request.POST['proyecto'])

        sprint_actual = Sprint.objects.get(id = request.POST['sprint'])
        diccionario['sprint']=sprint_actual


        #define some data
        total = 0

        for historia in sprint_actual.historias.all():
            total += historia.size

        plt.ylim(-1, total)
        lista = Registro.objects.filter(sprint=str(sprint_actual.id))
        listay = []
        listay.append(total)

        for registro in lista:

            total-=registro.horas
            listay.append(total)




        x = np.arange(0., len(lista) + 1, 1)
        y = np.array(listay)

        plt.xlim(0, len(lista)+1)
        plt.xlabel("Cargas de tareas")
        plt.ylabel("Horas restantes")
        plt.title("BurndownChart del Sprint " + sprint_actual.nombre)

        #plot data
        plt.plot(x, y, 'k', marker="o", color="green")
        savefig("grafico1.jpg")

        #show plot
        #plt.show()

        return render(request, self.template_name, diccionario)