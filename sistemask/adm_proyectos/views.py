from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Proyecto
from adm_usuarios.models import Usuario
from adm_roles.models import Rol
from sistemask.views import LoginView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .models import Cliente
from adm_flujos.models import Flujo
from adm_actividades.models import Actividad
from adm_historias.models import Historia

from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import auth

from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class ProyectoView(TemplateView):
    """
    Esta clase hereda de TemplateView
    Se encarga se realizar al autenticacion del usuario y lo lleva a la pagina de inicio

    """
    template_name = 'Proyecto.html'
    context_object_name = 'lista_proyectos'


    def post(self, request, *args, **kwargs):
        """
        Esta funcion se encarga de la autenticacion del usuario, utiliza post para enviar los datos
        :param request:Peticion web
        :param args:Para mapear los argumentos posicionales a al tupla
        :param kwargs:Diccionario para mapear los argumentos de palabra clave
        :return: Si el usuario existe: Envia a la pagina principal "Proyecto.html"
                 Si el usuario no existe o es incorrecto: Envia un mensaje de error respectivamente

        """
        diccionario= {}                                                  #Diccionario para ser retornado en HTML
        #Login.html es la unica pagina que envia un 'user' en el diccionario de request.POST
        if 'user' in request.POST:
            existe= Usuario.objects.filter(username=request.POST['user'], estado=True)
            username = request.POST['user']
            password = request.POST['pass']
            if len(existe):
                if existe[0].password == request.POST['pass']:
                    user = authenticate(username=username, password=password)
                    diccionario[self.context_object_name]= Proyecto.objects.filter(activo= True)
                    diccionario['logueado']= existe[0]
                    login(request, user)
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
        """
        Esta funcion de encarga de retornar la pagina de login en caso que el acceso sea incorrecto, utiliza get para
        obtner la pagina.

        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: Retorna la misma pagina de login, con un error para indicar el acceso incorrecto
        """
        return render(request, LoginView.template_name, {'error':'Acceso Incorrecto'})



class CrearProyecto(LoginRequiredMixin, ProyectoView):
    """
    Esta clase es la engarcada de crear un proyecto
    Hereda de la clase ProyectoView
    """
    template_name = 'CrearProyecto.html'
    context_object_name = 'lista_proyectos'

    def post(self, request, *args, **kwargs):
        """
        Se encarga de crear un nuevo proyecto, teniendo como condicion que el usuario sea SM
        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: Retorna el formulacion para creacion de proyecto solo si el usuario poseer el rol de Scrum Master
                 En caso contrario retorna un mensaje de denegacion de acceso en la misma pagina de inicio.
        """
        #Usuario = request.user
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        diccionario[self.context_object_name]= Proyecto.objects.filter(activo= True)
        if len(Rol.objects.filter(nombre= 'Scrum Master', usuario= usuario_logueado)): #Si el logueado es Scrum Master
            diccionario['lista_usuarios']= Usuario.objects.filter(estado= True)
            del diccionario[self.context_object_name]
            return render(request, self.template_name, diccionario)
        else:
            diccionario['error']= 'No puedes realizar esta accion'
            return render(request, super(CrearProyecto, self).template_name, diccionario)


class CrearProyectoConfirm(CrearProyecto):
    """
    Para confirmar una creacion de proyecto. Boton "Guardar"
    """
    template_name = 'CrearProyectoConfirm.html'
    def post(self, request, *args, **kwargs):
        """
        Se encarga de verificar que el  nombre del proyecto no se repita
        para luego crear exitosamente el mismo

        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: Retorna un mensaje de error (en el caso que el nombre de proyecto ya exista) en la misma pagina
                 Retorna una pagina en donde se muestra la creacion existosa del proyecto.
        """
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
class EliminarProyecto(LoginRequiredMixin, ProyectoView):
    """
    Para eliminar un proyecto en forma logica. Boton "Eliminar"
    """
    template_name = 'EliminarProyecto.html'


    def post(self, request, *args, **kwargs):
        """
        Realiza la verificacion de roles y estado actual del proyecto,
        luego elimina si es posible.

        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: Retorna la pagina de eliminacion exitosa del proyecto (paso de activo a inactivo)
                 Retorna mensajes de error en caso de que el usuario no sea SM o el proyecto no este finalizado.
        """
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


'''#Generacion de Informe del Proyecto
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
        return render(request, self.template_name, diccionario)'''


#Iniciando Proyecto
class InicializarProyecto(LoginRequiredMixin, ProyectoView):
    """
    Dejar el proyecto en un estado inicial luego de su creacion
    """
    template_name = 'InicializarProyecto.html'
    def post(self, request, *args, **kwargs):
        """
        Realiza la verificacion de roles y estado del proyecto
        para comprobar si es posible inicializar

        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: Retorna la pagina de inicializacion en caso que el usuario tenga el rol correspondiente
                 Retorna mensajes de error en el caso que el usuario no posea el rol o el proyecto ya se encuentre inicializado
        """
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['logueado']= usuario_logueado
        diccionario[self.context_object_name]= Proyecto.objects.filter(activo= True)
        if len(Rol.objects.filter(nombre= 'Scrum Master', usuario= usuario_logueado)):
            if proyecto_actual.estado == 'N' or 'I':
                diccionario['lista_usuarios']= Usuario.objects.filter(estado= True)
                diccionario['lista_clientes']=Cliente.objects.filter(estado=True)
                diccionario['proyecto']= proyecto_actual
                del diccionario[self.context_object_name]
                return render(request, self.template_name, diccionario)
            else:
                diccionario['error']= 'El proyecto ya esta inicializado'
        else:
            diccionario['error']= 'No puede realizar esta accion'
        return render(request, super(InicializarProyecto, self).template_name, diccionario)

class InicializarProyectoConfirm(InicializarProyecto):
    """
    Confirma los datos de inicializacion del proyecto . Boton "Guardar"
    """
    template_name = 'InicializarProyectoConfirm.html'
    def post(self, request, *args, **kwargs):
        """
        Realiza la comprobacion de la fecha de inicio y fecha de fin del proyecto, en caso fecha_Fin<fecha_Inicio,
        se devuelve un error y se evita la inicializacion.
        Si las fechas son correctas se procede a obtener los miembros del equipo scrum.
        Luego se establece el estado del proyecto a I (Inicializado)

        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: Retorna en la misma pagina, un error en caso de detectar que las fechas no se corresponden.
                Retorna la pagina de inicializacion exitosa del proyecto.
        """
        diccionario= {}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        proyecto_detalles= Proyecto.objects.get(id= request.POST['proyecto'])
        proyecto_detalles.fecha_inicio= request.POST['fechaInicio']
        proyecto_detalles.fecha_fin= request.POST['fechaFin']
        if proyecto_detalles.fecha_fin < proyecto_detalles.fecha_inicio:
            diccionario['proyecto']= proyecto_detalles
            diccionario['lista_usuarios']= Usuario.objects.filter(estado= True)
            diccionario['lista_clientes']= Cliente.objects.filter(estado= True)
            diccionario['error']= 'ERROR - Fecha Inicio posterior a Fecha Fin'
            return render(request, super(InicializarProyectoConfirm, self).template_name, diccionario)
        #proyecto_detalles.sprints= request.POST['sprints']
        usuarios_miembros= request.POST.getlist('miembros[]')
        for i in usuarios_miembros: proyecto_detalles.scrum_team.add(Usuario.objects.get(username= i))
        new_cliente= Cliente.objects.get(username= request.POST['cliente'])
        proyecto_detalles.cliente= new_cliente

        proyecto_detalles.estado= 'I'
        proyecto_detalles.save()
        proyecto_detalles= Proyecto.objects.get(nombre= proyecto_detalles.nombre)

        return render(request, self.template_name, diccionario)


class Ingresar(LoginRequiredMixin, TemplateView):
    """
    Ingresar al entorno de un proyecto en particular
    Se listan las operaciones realizables
    """
    template_name = 'InicioProyecto.html'

    def post(self, request, *args, **kwargs):
        """

        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return:Retorna la pagina de inicio del proyecto.
        """
        diccionario = {}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        proyecto_detalles= Proyecto.objects.get(id= request.POST['proyecto'])
        diccionario['proyecto']= proyecto_detalles
        return render(request,self.template_name, diccionario)

class ModificarProyecto(LoginRequiredMixin, ProyectoView):
    """
    Modificacion de algunos campos de proyecto
    """
    template_name = 'ModificarProyecto.html'
    context_object_name = 'lista_proyectos'
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
        diccionario[self.context_object_name]= Proyecto.objects.filter(activo= True)
        if len(Rol.objects.filter(nombre= 'Scrum Master', usuario= usuario_logueado)): #Si el logueado es SM
            diccionario['lista_usuarios']= Usuario.objects.filter(estado= True)
            del diccionario[self.context_object_name]
            return render(request, self.template_name, diccionario)
        else:
            diccionario['error']= 'No puedes realizar esta accion'
            return render(request, super(ModificarProyecto, self).template_name, diccionario)

class ModificarProyectoConfirm(ModificarProyecto):
    """
    Confirma la modificacion de un proyecto
    """
    template_name = 'ModificarProyectoConfirm.html'
    def post(self, request, *args, **kwargs):
        """
        Realiza la verifiacion de que el nombre del proyecto sea unico y luego actualiza los datos.

        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: Retorna un mensaje de error, en el caso de que el nombre del proyecto sea repetido.
                Retorna la pagina de modificacion exitosa del proyecto
        """
        diccionario= {}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado

        modificacion= Proyecto.objects.get(id= request.POST['proyecto'])
        modificacion_nombre= request.POST['nombre_proyecto']

        existe= Proyecto.objects.filter(nombre= modificacion_nombre)
        if len(existe) and existe[0]!=modificacion:
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


class Generarkanban(LoginRequiredMixin, ProyectoView):
    template_name = 'Generarkanban.html'
    def post(self, request, *args, **kwargs):
        """
        Realiza la verifiacion de que el usuario posea el permiso y luego muestra la tabla kanban
        que pertenece al proyecto actual.

        Para la tabla se llevan la lista de flujos del proyecto actual
        luego apartir de la lista de flujos, se obtienen la lista de actividades del
        flujo y se van mostrando secuencialmente como fueron ordenadas.

        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: Retorna un mensaje de error, en el caso de que el usuario no posea permisos para ver la tabla
                Retorna la pagina donde se puede observar la tabla kanban del proyecto

        """
        diccionario = {}
        proyecto_actual = Proyecto.objects.get(id=request.POST['proyecto'])
        diccionario['proyecto']=proyecto_actual
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado

        lista_flujos = Flujo.objects.filter(proyecto=proyecto_actual, activo=True).order_by('nombre')
        lista_historias = Historia.objects.filter(proyecto=proyecto_actual, activo=True).order_by('nombre')
        diccionario['flujos']=lista_flujos
        diccionario['historias']=lista_historias

        actividades=[]
        for i in lista_flujos:
            actividades = Actividad.objects.filter(proyecto=proyecto_actual, estado=True).order_by('secuencia')


        diccionario['actividades_flujo']=actividades



        return render(request, self.template_name, diccionario)

class ProductBacklog(LoginRequiredMixin, ProyectoView):
    template_name = 'ProductBacklog.html'
    def post(self, request, *args, **kwargs):
        """
        Realiza la verifiacion de que el usuario posea el permiso y luego muestra el product backlog
        que pertenece al proyecto actual.

        Para el product backlog se lleva la lista de historias de usuario priorizadas del proyecto
        dando las opciones de realizar distintos tipos de filtros sobre ellos.

        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: Retorna un mensaje de error, en el caso de que el usuario no posea permisos para ver el product backlog
                Retorna la pagina donde se puede observar el productBacklog del proyecto

        """
        diccionario = {}
        proyecto_actual = Proyecto.objects.get(id=request.POST['proyecto'])
        diccionario['proyecto']=proyecto_actual
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado

        lista_historias = Historia.objects.filter(proyecto=proyecto_actual, activo=True).order_by('nombre')
        diccionario['historias']=lista_historias


        return render(request, self.template_name, diccionario)

class ProductBacklogPri(LoginRequiredMixin, ProyectoView):
    template_name = 'ProductBacklog.html'
    def post(self, request, *args, **kwargs):
        """
        Realiza la verifiacion de que el usuario posea el permiso y luego muestra el product backlog
        que pertenece al proyecto actual.

        Para el product backlog se lleva la lista de historias de usuario priorizadas del proyecto
        dando las opciones de realizar distintos tipos de filtros sobre ellos.

        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: Retorna un mensaje de error, en el caso de que el usuario no posea permisos para ver el product backlog
                Retorna la pagina donde se puede observar el productBacklog del proyecto

        """
        diccionario = {}
        proyecto_actual = Proyecto.objects.get(id=request.POST['proyecto'])
        diccionario['proyecto']=proyecto_actual
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado

        lista_historias = Historia.objects.filter(proyecto=proyecto_actual, activo=True).order_by('prioridad')
        diccionario['historias']=lista_historias


        return render(request, self.template_name, diccionario)

class ProductBacklogNeg(LoginRequiredMixin, ProyectoView):
    template_name = 'ProductBacklog.html'
    def post(self, request, *args, **kwargs):
        """
        Realiza la verifiacion de que el usuario posea el permiso y luego muestra el product backlog
        que pertenece al proyecto actual.

        Para el product backlog se lleva la lista de historias de usuario priorizadas del proyecto
        dando las opciones de realizar distintos tipos de filtros sobre ellos.

        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: Retorna un mensaje de error, en el caso de que el usuario no posea permisos para ver el product backlog
                Retorna la pagina donde se puede observar el productBacklog del proyecto

        """
        diccionario = {}
        proyecto_actual = Proyecto.objects.get(id=request.POST['proyecto'])
        diccionario['proyecto']=proyecto_actual
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado

        lista_historias = Historia.objects.filter(proyecto=proyecto_actual, activo=True).order_by('val_negocio')
        diccionario['historias']=lista_historias


        return render(request, self.template_name, diccionario)

class ProductBacklogTec(LoginRequiredMixin, ProyectoView):
    template_name = 'ProductBacklog.html'
    def post(self, request, *args, **kwargs):
        """
        Realiza la verifiacion de que el usuario posea el permiso y luego muestra el product backlog
        que pertenece al proyecto actual.

        Para el product backlog se lleva la lista de historias de usuario priorizadas del proyecto
        dando las opciones de realizar distintos tipos de filtros sobre ellos.

        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: Retorna un mensaje de error, en el caso de que el usuario no posea permisos para ver el product backlog
                Retorna la pagina donde se puede observar el productBacklog del proyecto

        """
        diccionario = {}
        proyecto_actual = Proyecto.objects.get(id=request.POST['proyecto'])
        diccionario['proyecto']=proyecto_actual
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado

        lista_historias = Historia.objects.filter(proyecto=proyecto_actual, activo=True).order_by('val_tecnico')
        diccionario['historias']=lista_historias


        return render(request, self.template_name, diccionario)
