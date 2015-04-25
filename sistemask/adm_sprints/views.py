from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Proyecto
from adm_usuarios.models import Usuario
from adm_roles.models import Rol
from sistemask.views import LoginView
from adm_sprints.models import Sprint
from adm_historias.models import Historia

from adm_proyectos.views import LoginRequiredMixin

class SprintView(TemplateView):

    template_name = 'Sprint.html'
    context_object_name = 'lista_sprints'

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
        if len(Rol.objects.filter(nombre= 'Scrum Master', usuario= usuario_logueado)): #Si el logueado es Scrum Master
            #diccionario['lista_usuarios']= Usuario.objects.filter(estado= True)
            #del diccionario[self.context_object_name]
            return render(request, self.template_name, diccionario)
        else:
            diccionario['error']= 'No puedes realizar esta accion'
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
            diccionario['error']= 'Nombre de proyecto ya existe'
            return render(request, super(CrearSprintConfirm, self).template_name, diccionario)
        else:
            #Creamos el sprint
            nuevo_sprint= Sprint()
            nuevo_sprint.nombre= new_nombre
            nuevo_sprint.descripcion= request.POST['descripcion_sprint']
            nuevo_sprint.fecha_inicio = request.POST['fecha_inicio']
            nuevo_sprint.fecha_fin = request.POST['fecha_fin']
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

        if len(Rol.objects.filter(nombre= 'Scrum Master', usuario= usuario_logueado, activo= True)):
            if sprint_actual.estado=='P' and sprint_actual.asignado_h == False:
                sprint_actual.activo= False
                sprint_actual.save()
                del diccionario[self.context_object_name]  #No hace falta enviar la lista de proyectos
                return render(request, self.template_name, diccionario)
            else:
                diccionario['error']= 'Sprint Activado o con Historias de Usuario asignadas- No se puede eliminar'
        else:
            diccionario['error']= 'No puedes realizar esta accion'
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

        if len(Rol.objects.filter(nombre= 'Scrum Master', usuario= usuario_logueado)): #Si el logueado es SM
            diccionario['lista_usuarios']= Usuario.objects.filter(estado= True)
            del diccionario[self.context_object_name]
            return render(request, self.template_name, diccionario)
        else:
            diccionario['error']= 'No puedes realizar esta accion'
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

        existe= Sprint.objects.filter(nombre= modificacion_nombre)
        if existe:
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

class ActivarSprint(LoginRequiredMixin, SprintView):
    """
    pasar un sprint del estado P(Planeado) al estado A(Activo)
    """

    template_name = 'ActivarSprint.html'
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
        sprint_actual = Sprint.objects.get(id= request.POST['sprint'])

        proyecto_actual = Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario[self.context_object_name]= Sprint.objects.filter(activo= True, proyecto= proyecto_actual)

        if len(Rol.objects.filter(nombre= 'Scrum Master', usuario= usuario_logueado)):
            if sprint_actual.estado == 'P':
                sprint_actual.estado = 'A'
                sprint_actual.save()
            else:
                sprint_actual.estado = 'P'
                sprint_actual.save()
            return render(request, self.template_name, diccionario)

        else:
            diccionario['error'] = 'No puedes realizar esta accion'
            return render(request, super(ActivarSprint, self).template_name, diccionario)



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
        diccionario['historias']= Historia.objects.filter(activo= True, proyecto= proyecto_actual, asignado_p=False)

        sprint_actual = Sprint.objects.get(id = request.POST['sprint'])
        diccionario['sprint']=sprint_actual

        if len(Rol.objects.filter(nombre= 'Scrum Master', usuario= usuario_logueado)):
             return render(request, self.template_name, diccionario)

        else:
             diccionario['error'] = 'No puedes realizar esta accion'
             return render(request, super(AsignarHistorias, self).template_name, diccionario)


class AsignarHistoriasConfirm(LoginRequiredMixin, SprintView):
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
            sprint_detalles.historias.add(Historia.objects.get(nombre=i))
            Historia_asignada = Historia.objects.get(nombre=i)
            Historia_asignada.sprint = id_sprint
            Historia_asignada.asignado_p = True
            Historia_asignada.save()

        sprint_detalles.save()

        return render(request, self.template_name, diccionario)