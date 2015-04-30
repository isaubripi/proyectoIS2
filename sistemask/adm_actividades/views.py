
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Proyecto
from adm_usuarios.models import Usuario
from adm_roles.models import Rol
from sistemask.views import LoginView
from adm_sprints.models import Sprint
from adm_historias.models import Historia
from adm_flujos.models import Flujo
from adm_actividades.models import Actividad
from adm_proyectos.views import ProyectoView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from adm_proyectos.views import LoginRequiredMixin

# Create your views here.



class ActividadView(TemplateView):

    template_name = 'Actividad.html'
    context_object_name = 'lista_actividades'

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """

        :param request: Peticion Web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return:Pagina de inicio de Adm actividades.

        Esta funcion presenta todas las operacion que se pueden realizar sobre las actividades de un flujo
        ABM y establecer secuencia
        """

        diccionario= {}
        #obtiene el proyecto actual
        flujo_actual = Flujo.objects.get(id =request.POST['flujo'])
        id_flujo = request.POST['flujo']
        diccionario['flujo']=flujo_actual
        proyecto_actual = Proyecto.objects.get(id = request.POST['proyecto'])
        diccionario[self.context_object_name]= Actividad.objects.filter(estado= True, proyecto= proyecto_actual, flujo=id_flujo).order_by('secuencia')


        diccionario['logueado']= Usuario.objects.get(id=request.POST['login'])
        proyecto_detalles= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['proyecto']= proyecto_detalles
        return render(request, self.template_name, diccionario)


class CrearActividad(LoginRequiredMixin, ActividadView):
    """
    Esta clase es la engarcada de crear un sprint
    Hereda de la clase SprintView
    """
    template_name = 'CrearActividad.html'
    context_object_name = 'lista_sprints'
    def post(self, request, *args, **kwargs):
        """
        Se encarga de crear una nueva actividad, teniendo como condicion que el usuario sea SM
        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: Retorna el formulacion para creacion de sprint solo si el usuario posee el rol de Scrum Master
                 En caso contrario retorna un mensaje de denegacion de acceso en la misma pagina.
        """
        diccionario={}
        id_flujo = request.POST['flujo']
        diccionario['flujo']= Flujo.objects.get(id=request.POST['flujo'])
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual = Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        diccionario[self.context_object_name]= Actividad.objects.filter(estado= True, proyecto = proyecto_actual, flujo=id_flujo)
        if len(Rol.objects.filter(nombre= 'Scrum Master', usuario= usuario_logueado)): #Si el logueado es Scrum Master
            #diccionario['lista_usuarios']= Usuario.objects.filter(estado= True)
            #del diccionario[self.context_object_name]
            return render(request, self.template_name, diccionario)
        else:
            diccionario['error']= 'No puedes realizar esta accion'
            return render(request, super(CrearActividad, self).template_name, diccionario)


class CrearActividadConfirm(CrearActividad):
    """
    Para confirmar una creacion de sprint. Boton "Guardar"
    """
    template_name = 'CrearActividadConfirm.html'
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
        new_nombre= request.POST['nombre_actividad']
        id_flujo = request.POST['flujo']
        diccionario['flujo']=Flujo.objects.get(id=request.POST['flujo'])
        existe= Actividad.objects.filter(nombre= new_nombre, estado=True, proyecto=proyecto_actual, flujo=id_flujo)
        if existe:
            diccionario['lista_usuarios']= Usuario.objects.filter(estado= True)
            diccionario['error']= 'Nombre de Actividad ya existe'
            return render(request, super(CrearActividadConfirm, self).template_name, diccionario)
        else:
            #Creamos el sprint
            nueva_actividad= Actividad()
            nueva_actividad.nombre= new_nombre
            nueva_actividad.descripcion= request.POST['descripcion_actividad']
            new_proyecto= Proyecto.objects.get(id= request.POST['proyecto'])
            nueva_actividad.proyecto= new_proyecto
            nueva_actividad.flujo = id_flujo
            nueva_actividad.estado = True
            nueva_actividad.secuencia = 0
            nueva_actividad.save()

            lista = []
            #se agrega la actividad a el flujo

            flujo_actual = Flujo.objects.get(id=id_flujo)
            flujo_actual.actividades.add(nueva_actividad)
            flujo_actual.nro_actividades = flujo_actual.nro_actividades + 1

            flujo_actual.save()

            diccionario['actividad']=nueva_actividad
            return render(request, self.template_name, diccionario)

class EliminarActividad(LoginRequiredMixin, ActividadView):
    """
    Para eliminar una actividad forma logica. Boton "Eliminar"
    Solo se puede eliminar si la activida no posee historias de usuarios dentro
    """
    template_name = 'EliminarActividad.html'
    def post(self, request, *args, **kwargs):
        """
        Realiza la verificacion de roles,
        luego elimina si es posible.

        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: Retorna la pagina de eliminacion exitosa de la actividad (paso de activo a inactivo)
                 Retorna mensajes de error en caso de que el usuario no sea SM.
        """
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        #sprint_actual = Sprint.objects.get(id =request.POST['sprint'])
        actividad_actual = Actividad.objects.get(id=request.POST['actividad'])
        diccionario['actividad']=actividad_actual
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        diccionario['flujo']=Flujo.objects.get(id=request.POST['flujo'])
        #diccionario['sprint']= sprint_actual
        diccionario[self.context_object_name]= Sprint.objects.filter(activo= True, proyecto= proyecto_actual)

        if len(Rol.objects.filter(nombre= 'Scrum Master', usuario= usuario_logueado, activo= True)):
            if actividad_actual.asignado_h == False:
                actividad_actual.estado= False

                flujo_actual = Flujo.objects.get(id=request.POST['flujo'])
                flujo_actual.actividades.remove(actividad_actual)
                flujo_actual.nro_actividades = flujo_actual.nro_actividades - 1
                flujo_actual.save()

                actividad_actual.save()
                del diccionario[self.context_object_name]  #No hace falta enviar la lista de proyectos
                return render(request, self.template_name, diccionario)
            else:
                diccionario['error']= 'Actividad con Historias de Usuario Asignadas- No se puede eliminar'
        else:
            diccionario['error']= 'No puedes realizar esta accion'
        return render(request, super(EliminarActividad,self).template_name, diccionario)

class ModificarActividad(LoginRequiredMixin, ActividadView):
    """
    Modificacion de los campos del formulario actividad
    """
    template_name = 'ModificarActividad.html'
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
        #sprint_actual = Sprint.objects.get(id =request.POST['sprint'])
        #diccionario['sprint'] = sprint_actual
        actividad_actual = Actividad.objects.get(id=request.POST['actividad'])
        diccionario['actividad']=actividad_actual
        flujo_actual = Flujo.objects.get(id=request.POST['flujo'])
        diccionario['flujo']=flujo_actual

        proyecto_actual = Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario[self.context_object_name]= Sprint.objects.filter(activo= True, proyecto= proyecto_actual)

        if len(Rol.objects.filter(nombre= 'Scrum Master', usuario= usuario_logueado)): #Si el logueado es SM
            diccionario['lista_usuarios']= Usuario.objects.filter(estado= True)
            del diccionario[self.context_object_name]
            return render(request, self.template_name, diccionario)
        else:
            diccionario['error']= 'No puedes realizar esta accion'
            return render(request, super(ModificarActividad, self).template_name, diccionario)

class ModificarActividadConfirm(ModificarActividad):
    """
    Confirma la modificacion de una actividad
    """
    template_name = 'ModificarActividadConfirm.html'
    def post(self, request, *args, **kwargs):
        """
        Realiza la verificacion de que el nombre de la actividad sea unico y luego actualiza los datos.

        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: Retorna un mensaje de error, en el caso de que el nombre de la actividad sea repetido.
                Retorna la pagina de modificacion exitosa de la actividad
        """
        diccionario= {}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado

        diccionario['proyecto']= Proyecto.objects.get(id= request.POST['proyecto'])
        proyecto_actual = Proyecto.objects.get(id=request.POST['proyecto'])
        flujo_actual= Flujo.objects.get(id=request.POST['flujo'])
        diccionario['flujo']= flujo_actual


        modificacion= Actividad.objects.get(id= request.POST['actividad'])
        modificacion_nombre= request.POST['nombre_actividad']

        existe= Actividad.objects.filter(nombre= modificacion_nombre, estado=True, proyecto=proyecto_actual)
        if len(existe) and existe[0]!=modificacion:
            diccionario['lista_usuarios']= Usuario.objects.filter(estado= True)
            diccionario['error']= 'Nombre de actividad ya existe'
            return render(request, super(ModificarActividadConfirm, self).template_name, diccionario)
        else:
            #Modificamos  la actividad
            modificacion.nombre= modificacion_nombre
            modificacion.descripcion= request.POST['descripcion_actividad']

            modificacion.save()

            return render(request, self.template_name, diccionario)

class EstablecerSecuencia(LoginRequiredMixin, ActividadView):
    template_name = 'EstablecerSecuencia.html'
    def post(self, request, *args, **kwargs):
        """
        Realiza la verificacion de que el nombre de la actividad sea unico y luego actualiza los datos.

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
        flujo_actual= Flujo.objects.get(id=request.POST['flujo'])
        diccionario['flujo']= flujo_actual
        id_flujo = request.POST['flujo']
        proyecto_actual = Proyecto.objects.get(id=request.POST['proyecto'])
        actividad_actual = Actividad.objects.get(id=request.POST['actividad'])
        diccionario['actividad']=actividad_actual

        max = flujo_actual.nro_actividades

        lista = []
        lista_actividades = Actividad.objects.filter(proyecto=proyecto_actual, flujo=id_flujo, estado=True)

        for i in range(1,max+1):
            lista.append(i)
            for j in lista_actividades:
                if j.secuencia == i:
                    lista.remove(i)

        diccionario['actividades']=lista

        return render(request, self.template_name, diccionario)

class EstablecerSecuenciaConfirm(ActividadView):
    template_name = 'EstablecerSecuenciaConfirm.html'
    def post(self, request, *args, **kwargs):
        """
        Realiza la verificacion de que el nombre de la actividad sea unico y luego actualiza los datos.

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
        flujo_actual= Flujo.objects.get(id=request.POST['flujo'])
        diccionario['flujo']= flujo_actual
        id_flujo = request.POST['flujo']
        proyecto_actual = Proyecto.objects.get(id=request.POST['proyecto'])

        actividad_actual = Actividad.objects.get(id=request.POST['actividad'])
        actividad_actual.secuencia = request.POST['secuencia_actividad']
        actividad_actual.save()

        #ordenar la lista de actividades

        actividades_actuales = Actividad.objects.filter(estado=True, proyecto=proyecto_actual, flujo=id_flujo)
        lista_actividades = []

        for i in actividades_actuales:
            lista_actividades.append(i)

        # se quitan las actividades desordenadas
        for j in actividades_actuales:
            flujo_actual.actividades.remove(j)

        flujo_actual.save()

        # se agregan actividades ordenadas

        lista_actividades.sort(key=lambda x:x.secuencia, reverse=False)
        newlist = sorted(lista_actividades, key=lambda x: x.secuencia, reverse=False)


        for k in newlist:
            flujo_actual.actividades.add(k)

        flujo_actual.save()

        return render(request, self.template_name, diccionario)


