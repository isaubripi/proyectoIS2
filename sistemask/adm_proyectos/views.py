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
from adm_historias.models import Historia, Registro
from adm_sprints.models import Sprint

from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import auth

from django.utils.decorators import method_decorator

from reportlab.pdfgen import canvas
from django.http import HttpResponse

from reportlab.graphics.shapes import Drawing, Rect, String, Group, Line
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.textlabels import Label

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
        if len(Rol.objects.filter(crear_proyecto = True, usuario= usuario_logueado, activo=True)): #Si el logueado es Scrum Master
        #if len(usuario_logueado.roles.crear_proyecto == True):
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
            #cuando se crea un proyecto y se asigna al scrum master, seguidamente se crea un rol de scrum master y se asigna al scrum

            nuevo_scrum = Rol(nombre='Scrum_Master',
                    crear_proyecto =True,
                    modificar_proyecto = True,
                    eliminar_proyecto = True,
                    cerrar_proyecto = True,
                    inicializar_proyecto = True,
                    ingresar_proyecto = True,

                    crear_usuario = False,
                    modificar_usuario = False,
                    eliminar_usuario = False,
                    agregar_rol = True,
                    modificar_rol = True,
                    eliminar_rol = True,

                    generar_reporte = True,
                    generar_burndown = True,

                    asignar_usuario_inicial = True,
                    asignar_permisos_roles = True,
                    asignar_roles_usuario = True,
                    asignar_usuarios_proyecto = True,


                    agregar_sprint = True,
                    modificar_sprint = True,
                    eliminar_sprint = True,
                    activar_sprint = True,
                    asignar_historia = True,
                    desasignar_historia = True,
                    asignar_usuario_flujo = True,
                    asignar_equipo = True,
                    ver_sprintbacklog = True,

                    crear_actividad = True,
                    modificar_actividad = True,
                    eliminar_actividad = True,
                    establecer_secuencia = True,
                    restablecer_secuencia = True,

                    agregar_historia = True,
                    modificar_historia = True,
                    eliminar_historia = True,
                    cargar_horas = True,
                    ver_historial = True,
                    cancelar_historia = True,
                    release_historia = True,
                    ver_detalles = True,
                    cambiar_actividad_estado = True,
                    finalizar_historia = True,
                    horas_sprint = True,

                    crear_flujo = True,
                    modificar_flujo = True,
                    eliminar_flujo = True,
                    ver_tabla = True,
                    activo= True,
                    proyecto = nuevo_proyecto.id

            )

            nuevo_scrum.save()

            new_scrum_master.roles.add(nuevo_scrum)
            new_scrum_master.save()
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
        if len(Rol.objects.filter(eliminar_proyecto = True, usuario= usuario_logueado, activo= True)):
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
        rol_cliente = Rol.objects.filter(nombre='Cliente', proyecto=request.POST['proyecto'])
        if len(Rol.objects.filter(inicializar_proyecto = True , usuario= usuario_logueado)):
            if proyecto_actual.estado == 'N' or 'I':
                diccionario['lista_usuarios']= Usuario.objects.filter(estado= True)
                #diccionario['lista_clientes']=Cliente.objects.filter(estado=True)
                diccionario['lista_clientes'] = Usuario.objects.filter(roles=rol_cliente)
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
        #new_cliente= Cliente.objects.get(username= request.POST['cliente'])
        if request.POST['cliente']:
            new_cliente = Usuario.objects.get(username=request.POST['cliente'])
            cliente = Cliente(username=request.POST['cliente'])
            cliente.save()
            proyecto_detalles.cliente= cliente

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
        id_proyecto = request.POST['proyecto']
        roles = Rol.objects.filter(usuario=usuario_logueado, proyecto=id_proyecto)
        diccionario['roles']=roles
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
        if len(Rol.objects.filter(modificar_proyecto =True, usuario= usuario_logueado, activo=True)): #Si el logueado es SM
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
    template_ant = 'InicioProyecto.html'
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
        id_proyecto = request.POST['proyecto']
        diccionario['proyecto']=proyecto_actual
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado

        lista_flujos = Flujo.objects.filter(proyecto=proyecto_actual, activo=True).order_by('nombre')
        lista_historias = Historia.objects.filter(proyecto=proyecto_actual, activo=True).order_by('nombre')
        diccionario['flujos']=lista_flujos
        diccionario['historias']=lista_historias

        id_proyecto = request.POST['proyecto']
        roles = Rol.objects.filter(usuario=usuario_logueado, proyecto=id_proyecto)
        diccionario['roles']=roles

        actividades=[]
        for i in lista_flujos:
            actividades = Actividad.objects.filter(proyecto=proyecto_actual, estado=True).order_by('secuencia')


        diccionario['actividades_flujo']=actividades

        if len(Rol.objects.filter(ver_tabla = True, usuario=usuario_logueado, activo=True, proyecto=id_proyecto)):
            return render(request, self.template_name, diccionario)
        else:
            diccionario['error']= 'No posee el permiso'
            return render(request, self.template_ant, diccionario)





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

class CancelarHistoria(LoginRequiredMixin, TemplateView):

    """
    Para cancelar una historia. Boton "Cancelar"
    """
    template_name = 'CancelarHistoria.html'


    def post(self, request, *args, **kwargs):
        """
        Realiza la verificacion de roles y estado actual del proyecto,
        luego cancela si es posible.

        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: Retorna la pagina de cancelacion exitosa de la historia (cambio de estado)
                 Retorna mensajes de error en caso de que el usuario no posea los permisos.
        """
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        historia_actual = Historia.objects.get(id = request.POST['historia'])
        diccionario['proyecto']=proyecto_actual
        diccionario['logueado']= usuario_logueado

        lista_historias = Historia.objects.filter(proyecto=proyecto_actual, activo=True).order_by('nombre')
        diccionario['historias']=lista_historias

        #diccionario[self.context_object_name]= Proyecto.objects.filter(activo= True)
        if len(Rol.objects.filter(cancelar_historia = True, usuario= usuario_logueado, activo= True)):
            historia_actual.estado_scrum = 'Cancelado'
            historia_actual.save()
            return render(request, self.template_name, diccionario)
        else:
            diccionario['error']= 'No posee permiso para cancelar historia'
            return render(request, super(CancelarHistoria,self).template_name, diccionario)

class ReleaseHistoria(LoginRequiredMixin, TemplateView):

    """
    Para hacer release a una historia. Boton "Release"
    """
    template_name = 'ReleaseHistoria.html'


    def post(self, request, *args, **kwargs):
        """
        Realiza la verificacion de roles y estado actual del proyecto,
        luego cancela si es posible.

        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: Retorna la pagina de release exitosa de la historia (cambio de estado scrum)
                 Retorna mensajes de error en caso de que el usuario no posea los permisos.
        """
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        historia_actual = Historia.objects.get(id = request.POST['historia'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual
        diccionario['historia'] = historia_actual

        lista_historias = Historia.objects.filter(proyecto=proyecto_actual, activo=True).order_by('nombre')
        diccionario['historias']=lista_historias

        lista = Registro.objects.filter(id_historia=historia_actual, activo=True)
        diccionario['registros'] = lista

        #diccionario[self.context_object_name]= Proyecto.objects.filter(activo= True)
        if len(Rol.objects.filter(release_historia = True, usuario= usuario_logueado, activo= True)):

            return render(request, self.template_name, diccionario)
        else:
            diccionario['error']= 'No posee permiso para finalizar la historia'
            return render(request, super(ReleaseHistoria,self).template_name, diccionario)


class ReleaseConfirm(LoginRequiredMixin, TemplateView):
    """
    Para hacer release a una historia. Boton "Release"
    Pasa del estado "Pendiente" a "Released"

    """

    template_name = 'ReleaseConfirm.html'

    def post(self, request, *args, **kwargs):
        """
        Realiza la verificacion de roles y estado actual del proyecto,
        luego cancela si es posible.

        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: Retorna la pagina de release exitosa de la historia (cambio de estado scrum)
                 Retorna mensajes de error en caso de que el usuario no posea los permisos.
        """
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        proyecto_actual= Proyecto.objects.get(id= request.POST['proyecto'])
        historia_actual = Historia.objects.get(id = request.POST['historia'])
        diccionario['logueado']= usuario_logueado
        diccionario['proyecto']= proyecto_actual

        lista_historias = Historia.objects.filter(proyecto=proyecto_actual, activo=True).order_by('nombre')
        diccionario['historias']=lista_historias

        #diccionario[self.context_object_name]= Proyecto.objects.filter(activo= True)
        if len(Rol.objects.filter(release_historia = True, usuario= usuario_logueado, activo= True)):
            historia_actual.estado_scrum = 'Released'
            historia_actual.save()
            return render(request, self.template_name, diccionario)
        else:
            diccionario['error']= 'No posee permiso para finalizar la historia'
            return render(request, super(ReleaseHistoria,self).template_name, diccionario)



class GenerarReporte(LoginRequiredMixin, ProyectoView):

    template_name = 'InicioProyecto.html'
    def post(self, request, *args, **kwargs):
        """

        :param request: peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return:retorna el informe en formato pdf y se visualiza con al aplicacion
        """
        proyecto_actual= Proyecto.objects.get(id=request.POST['proyecto'])


        import os
        import datetime
        # Obtenemos de platypus las clases Paragraph, para escribir parrafos Image, para insertar imagenes y SimpleDocTemplate para definir el DocTemplate. Ademas importamos Spacer, para incluir espacios .
        from reportlab.platypus import Paragraph
        from reportlab.platypus import SimpleDocTemplate
        from reportlab.platypus import Spacer
        from reportlab.platypus import Table

        # Importamos clase de hoja de estilo de ejemplo.
        from reportlab.lib.styles import getSampleStyleSheet

        # Se importa el tamanho de la hoja y los colores
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors

        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['proyecto'] = proyecto_actual
        diccionario['logueado'] = usuario_logueado
        id_proyecto = request.POST['proyecto']
        roles = Rol.objects.filter(usuario=usuario_logueado, proyecto=id_proyecto)
        diccionario['roles']=roles

        # Creamos un PageTemplate de ejemplo.
        estiloHoja = getSampleStyleSheet()

        #Inicializamos la lista Platypus Story.
        story = []

        #Definimos como queremos que sea el estilo de la PageTemplate.
        cabecera = estiloHoja['Heading5']

        #No se hara un salto de pagina despues de escribir la cabecera (valor 1 en caso contrario).
        cabecera.pageBreakBefore=0

        # Se quiere que se empiece en la primera pagina a escribir. Si es distinto de 0 deja la primera hoja en blanco.
        cabecera.keepWithNext=0



        # Color de la cabecera.
        cabecera.backColor=colors.white
        cabecera.spaceAfter = 0
        cabecera.spaceBefore = 0

        titulo = estiloHoja['Heading1']
        titulo.pageBreakBefore=0
        titulo.keepWithNext=0
        titulo.backColor=colors.orange
        titulo.spaceAfter = 50
        titulo.spaceBefore = 50
        titulo.rightMargin = 50

        parrafo = Paragraph('SISTEMA DE GESTION DE PROYECTOS AGILES SK',titulo)
        story.append(parrafo)
        parrafo = Paragraph('REPORTE DEL PROYECTO: '+ proyecto_actual.nombre,cabecera)
        story.append(parrafo)
        parrafo = Paragraph('-'*193,cabecera)
        story.append(parrafo)

        #parrafo = Paragraph('1. CANTIDAD DE TRABAJO EN CURSO POR EQUIPO', cabecera)
        #story.append(parrafo)
        story.append(Spacer(0,20))

        historias = Historia.objects.filter(proyecto=proyecto_actual, activo= True)
        lista = []
        lista.append(['1. CANTIDAD DE TRABAJO EN CURSO POR EQUIPO', ' ', ' '])
        lista.append([' ', ' ', ' '])
        lista.append(['Equipo', 'Cantidad', 'Estado'])
        cant=0
        for j in historias:
            if(j.sprint):
                sprint = j.sprint
                sprint_actual = Sprint.objects.get(id=sprint)
                if sprint_actual.estado == 'En Ejecucion' and j.estado_scrum=='Pendiente':
                    cant = cant + 1

        #team = []
        #for k in proyecto_actual.scrum_team.all():
        #    team.append(k.username)

        #sprint_ejecucion = Sprint.objects.get(proyecto=proyecto_actual, activo=True, estado='En Ejecucion')
        if cant==0:
            estado = 'Completado'
        else:
            estado= 'En Progreso'

        lista.append([proyecto_actual.scrum_team.all(), cant, estado])

        t=Table( lista, style = [
                       ('GRID',(0,0),(-1,-1),0.5,colors.white),
                       ('BOX',(0,0),(-1,-1),2,colors.white),
                       ('SPAN',(0,0),(-1,0)),
                       ('ROWBACKGROUNDS', (0, 3), (-1, -1), (colors.Color(0.9, 0.9, 0.9),colors.white)),
                       ('BACKGROUND', (0, 2), (-1, 2), colors.rgb2cmyk(r=6,g=62,b=193)),
                       ('BACKGROUND', (0, 1), (-1, 1), colors.white),
                       ('LINEABOVE',(0,0),(-1,0),1.5,colors.black),
                       ('LINEBELOW',(0,0),(-1,0),1.5,colors.black),
                       ('SIZE',(0,0),(-1,0),12),
                       ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                       ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
                       ('TEXTCOLOR', (0, 2), (-1, 2), colors.white),
                       ]
              )

        # Y lo incluimos en el story.
        story.append(t)

        # Dejamos espacio.
        story.append(Spacer(0,20))

        parrafo = Paragraph('-'*193,cabecera)
        story.append(parrafo)

        story.append(Spacer(0,20))

        historias = Historia.objects.filter(proyecto=proyecto_actual, activo= True)
        lista = []
        lista.append(['2. CANTIDAD DE TRABAJO POR USUARIO: PENDIENTE, EN CURSO, FINALIZADO', ' ', ' ', ' '])
        lista.append([' ', ' ', ' ', ' '])
        lista.append(['Usuario', 'Pendiente', 'En Curso', 'Finalizado'])


        for i in proyecto_actual.scrum_team.all():
            cant_pen = 0
            cant_cur = 0
            cant_fin = 0

            for j in historias:
                if i == j.asignado:
                    if j.estado_scrum== 'Pendiente' and j.estado_sprint=='No iniciado':
                        cant_pen = cant_pen + 1
                    elif j.estado_sprint == 'En Progreso' and j.estado_scrum=='Pendiente':
                        cant_cur = cant_cur + 1
                    elif j.estado_scrum == 'Released' or j.estado_sprint=='Completada':
                        cant_fin = cant_fin + 1

            lista.append([i.username, cant_pen, cant_cur, cant_fin])

        t=Table( lista, style = [
                       ('GRID',(0,0),(-1,-1),0.5,colors.white),
                       ('BOX',(0,0),(-1,-1),2,colors.white),
                       ('SPAN',(0,0),(-1,0)),
                       ('ROWBACKGROUNDS', (0, 3), (-1, -1), (colors.Color(0.9, 0.9, 0.9),colors.white)),
                       ('BACKGROUND', (0, 2), (-1, 2), colors.rgb2cmyk(r=6,g=62,b=193)),
                       ('BACKGROUND', (0, 1), (-1, 1), colors.white),
                       ('LINEABOVE',(0,0),(-1,0),1.5,colors.black),
                       ('LINEBELOW',(0,0),(-1,0),1.5,colors.black),
                       ('SIZE',(0,0),(-1,0),12),
                       ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                       ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
                       ('TEXTCOLOR', (0, 2), (-1, 2), colors.white),
                       ]
              )

        # Y lo incluimos en el story.
        story.append(t)

        # Dejamos espacio.
        story.append(Spacer(0,20))

        parrafo = Paragraph('-'*193,cabecera)
        story.append(parrafo)
        story.append(Spacer(0,20))

        historias = Historia.objects.filter(proyecto=proyecto_actual, activo= True).order_by('prioridad')
        lista = []
        lista.append(['3. LISTA CLASIFICADA POR ORDEN DE PRIORIDAD PARA COMPLETAR EL PROYECTO', ' ', ' '])
        lista.append([' ', ' ', ' '])
        lista.append(['Prioridad', 'Actividad', 'Estado'])



        for j in historias:
            lista.append([j.prioridad, j.nombre, j.estado_scrum])

        t=Table( lista, style = [
                       ('GRID',(0,0),(-1,-1),0.5,colors.white),
                       ('BOX',(0,0),(-1,-1),2,colors.white),
                       ('SPAN',(0,0),(-1,0)),
                       ('ROWBACKGROUNDS', (0, 3), (-1, -1), (colors.Color(0.9, 0.9, 0.9),colors.white)),
                       ('BACKGROUND', (0, 2), (-1, 2), colors.rgb2cmyk(r=6,g=62,b=193)),
                       ('BACKGROUND', (0, 1), (-1, 1), colors.white),
                       ('LINEABOVE',(0,0),(-1,0),1.5,colors.black),
                       ('LINEBELOW',(0,0),(-1,0),1.5,colors.black),
                       ('SIZE',(0,0),(-1,0),12),
                       ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                       ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
                       ('TEXTCOLOR', (0, 2), (-1, 2), colors.white),
                       ]
              )

        # Y lo incluimos en el story.
        story.append(t)

        # Dejamos espacio.
        story.append(Spacer(0,20))


        # Dejamos espacio.
        story.append(Spacer(0,20))

        parrafo = Paragraph('-'*193,cabecera)
        story.append(parrafo)
        story.append(Spacer(0,20))


        story.append(Spacer(0,20))

        historias = Historia.objects.filter(proyecto=proyecto_actual, activo= True).order_by('prioridad')
        lista = []
        lista.append(['4. TIEMPO ESTIMADO POR PROYECTO Y EJECUCION', ' ', ' '])
        lista.append([' ', ' ', ' ', ' '])
        lista.append(['Sprint', 'Descripcion', 'Tiempo Estimado en dias', 'Tiempo en Ejecucion en dias'])


        sprints_proyecto = Sprint.objects.filter(proyecto=proyecto_actual, activo=True).order_by("nombre")


        #lista1 = []
        for j in sprints_proyecto:
            lista1=[]

            tareas = Registro.objects.filter(proyecto=proyecto_actual,sprint=j.id ).order_by("-id")
            for k in tareas:
                lista1.append(k)

            if len(lista1):
                fecha_ultima_tarea = lista1[0].fecha1

                tiempo_ejecutado = fecha_ultima_tarea - j.fecha_inicio

            else:
                tiempo_ejecutado = j.fecha_inicio - j.fecha_inicio

            lista.append([j.nombre, j.descripcion, j.duracion, tiempo_ejecutado.days])

        t=Table( lista, style = [
                       ('GRID',(0,0),(-1,-1),0.5,colors.white),
                       ('BOX',(0,0),(-1,-1),2,colors.white),
                       ('SPAN',(0,0),(-1,0)),
                       ('ROWBACKGROUNDS', (0, 3), (-1, -1), (colors.Color(0.9, 0.9, 0.9),colors.white)),
                       ('BACKGROUND', (0, 2), (-1, 2), colors.rgb2cmyk(r=6,g=62,b=193)),
                       ('BACKGROUND', (0, 1), (-1, 1), colors.white),
                       ('LINEABOVE',(0,0),(-1,0),1.5,colors.black),
                       ('LINEBELOW',(0,0),(-1,0),1.5,colors.black),
                       ('SIZE',(0,0),(-1,0),12),
                       ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                       ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
                       ('TEXTCOLOR', (0, 2), (-1, 2), colors.white),
                       ]
              )

        # Y lo incluimos en el story.
        story.append(t)


        # Dejamos espacio.
        story.append(Spacer(0,20))

        duracion_estimada = []
        duracion_ejecutada = []
        nombres = []
        #lista2 = []


        for j in sprints_proyecto:
            lista2=[]

            tareas = Registro.objects.filter(proyecto=proyecto_actual,sprint=j.id ).order_by("-id")
            for k in tareas:
                lista2.append(k)

            if len(lista2):
                fecha_ultima_tarea = lista2[0].fecha1

                tiempo_ejecutado = fecha_ultima_tarea - j.fecha_inicio
            else:
                tiempo_ejecutado = j.fecha_inicio - j.fecha_inicio

            duracion_estimada.append(j.duracion)
            nombres.append(j.nombre)
            duracion_ejecutada.append(tiempo_ejecutado.days)

        #cantSprints = sprints_proyecto.count()

        d = Drawing(400, 200)
        width=400
        height=200
        d.height=height
        d.width=width
        d.add(VerticalBarChart(), name='chart')
        d.add(String(100,180,'Duracion de Sprints del Proyecto en dias'), name='title')


        d.chart.x = 50
        d.chart.y = 20
        d.chart.width = d.width - 20
        d.chart.height = d.height - 40
        d.chart.valueAxis.valueMin = 0
        d.chart.valueAxis.valueMax = 50
        d.chart.valueAxis.valueStep = 10
        d.chart.categoryAxis.categoryNames = nombres
        d.chart.bars[0].fillColor = colors.orange
        d.chart.bars[1].fillColor = colors.darkblue

        d.title.fontName = 'Helvetica-Bold'
        d.translate(50,-10)
        d.title.fontSize = 12

        data = [duracion_estimada, duracion_ejecutada]

        lab1 = Label()
        lab1.setOrigin(100,90)
        lab1.angle = 0
        lab1.dx = 370  # desplazamiento en x
        lab1.dy = -20  # desplazamiento en y
        lab1.boxStrokeColor = colors.darkorange
        lab1.setText('Naranja: Tiempo \nEstimado')

        lab2 = Label()
        lab2.setOrigin(100,90)
        lab2.angle = 0
        lab2.dx = 370  # desplazamiento en x
        lab2.dy = 20  # desplazamiento en y
        lab2.boxStrokeColor = colors.darkblue
        lab2.setText('Azul: Tiempo en \nEjecucion')

        d.add(lab1)
        d.add(lab2)

        d.chart.data = data


        story.append(d)

         # Dejamos espacio.
        story.append(Spacer(0,20))

        parrafo = Paragraph('-'*193,cabecera)
        story.append(parrafo)

        historias = Historia.objects.filter(proyecto=proyecto_actual, activo= True).order_by('prioridad')
        lista = []
        lista.append(['5. BACKLOG DEL PRODUCTO', ' ', ' ', ' '])
        lista.append([' ', ' ', ' ', ' '])
        lista.append(['Nombre', 'Descripcion', 'Orden', 'Estado'])

        story.append(Spacer(0,20))

        for j in historias:
            lista.append([j.nombre, j.descripcion, j.prioridad, j.estado_scrum])

        t=Table( lista, style = [
                       ('GRID',(0,0),(-1,-1),0.5,colors.white),
                       ('BOX',(0,0),(-1,-1),2,colors.white),
                       ('SPAN',(0,0),(-1,0)),
                       ('ROWBACKGROUNDS', (0, 3), (-1, -1), (colors.Color(0.9, 0.9, 0.9),colors.white)),
                       ('BACKGROUND', (0, 2), (-1, 2), colors.rgb2cmyk(r=6,g=62,b=193)),
                       ('BACKGROUND', (0, 1), (-1, 1), colors.white),
                       ('LINEABOVE',(0,0),(-1,0),1.5,colors.black),
                       ('LINEBELOW',(0,0),(-1,0),1.5,colors.black),
                       ('SIZE',(0,0),(-1,0),12),
                       ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                       ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
                       ('TEXTCOLOR', (0, 2), (-1, 2), colors.white),
                       ]
              )

        # Y lo incluimos en el story.
        story.append(t)

        # Dejamos espacio.
        story.append(Spacer(0,20))

         # Dejamos espacio.
        story.append(Spacer(0,20))

        parrafo = Paragraph('-'*193,cabecera)
        story.append(parrafo)
        story.append(Spacer(0,20))

        historias = Historia.objects.filter(proyecto=proyecto_actual, activo= True).order_by('prioridad')
        lista = []
        lista.append(['6. BACKLOG DEL SPRINT', ' ', ' ', ' ', ' '])
        lista.append([' ', ' ', ' ', ' ', ' '])
        lista.append(['Nombre', 'Descripcion', 'Actividad','Estado Kanban',  'Flujo'])


        for j in historias:
            if(j.sprint):
                sprint = j.sprint
                sprint_actual = Sprint.objects.get(id=sprint)
                if sprint_actual.estado == 'En Ejecucion':
                    lista.append([j.nombre, j.descripcion, j.actividad, j.estado, j.flujo])

        t=Table( lista, style = [
                       ('GRID',(0,0),(-1,-1),0.5,colors.white),
                       ('BOX',(0,0),(-1,-1),2,colors.white),
                       ('SPAN',(0,0),(-1,0)),
                       ('ROWBACKGROUNDS', (0, 3), (-1, -1), (colors.Color(0.9, 0.9, 0.9),colors.white)),
                       ('BACKGROUND', (0, 2), (-1, 2), colors.rgb2cmyk(r=6,g=62,b=193)),
                       ('BACKGROUND', (0, 1), (-1, 1), colors.white),
                       ('LINEABOVE',(0,0),(-1,0),1.5,colors.black),
                       ('LINEBELOW',(0,0),(-1,0),1.5,colors.black),
                       ('SIZE',(0,0),(-1,0),12),
                       ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                       ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
                       ('TEXTCOLOR', (0, 2), (-1, 2), colors.white),
                       ]
              )

        # Y lo incluimos en el story.
        story.append(t)

        # Dejamos espacio.
        story.append(Spacer(0,20))



        # Incluimos un Flowable, que en este caso es un parrafo.

        cabecera2 = estiloHoja['Heading3']
        cabecera2.pageBreakBefore=0
        cabecera2.keepWithNext=0
        cabecera2.backColor=colors.white

        parrafo = Paragraph('   ',cabecera2)
        # Lo incluimos en el Platypus story.
        story.append(parrafo)

         # Dejamos espacio.
        story.append(Spacer(0,20))

        # Creamos un DocTemplate en una hoja DIN A4, en la que se muestra el texto enmarcado (showBoundary=1) por un recuadro.
        doc=SimpleDocTemplate("Rep_items.pdf",pagesize=A4, rightMargin=1, leftMargin=1, topMargin=0, bottomMargin=0)

        parrafo = Paragraph('-'*193,cabecera)
        story.append(parrafo)
        parrafo = Paragraph('Fin del Informe' + ' '*100 + '('+str(datetime.date.today()) + ')' ,cabecera)
        story.append(parrafo)

        # Construimos el Platypus story.
        doc.build(story)



        image_data = open("Rep_items.pdf", "rb").read()
        if len(Rol.objects.filter(generar_reporte = True, usuario= usuario_logueado, activo= True,proyecto=request.POST['proyecto'])):
            return HttpResponse(image_data, mimetype="application/pdf")
        else:
            diccionario['error']= 'No posee permiso para generar el reporte'
            return render(request, self.template_name, diccionario)



class FinalizarProyecto(LoginRequiredMixin, ProyectoView):

    template_name = 'FinalizarProyecto.html'
    def post(self, request, *args, **kwargs):
        """
        Realiza la verificacion de que el usuario posea el permiso y luego muestra historias
        que pertenecen al proyecto actual.

        Para el product backlog se lleva la lista de historias de usuario priorizadas del proyecto
        dando las opciones de realizar distintos tipos de filtros sobre ellos.

        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: Retorna un mensaje de error, en el caso de que el usuario no posea permisos para finalizar o no se pueda
                Retorna la pagina donde se puede observar la finalizacion correcta

        """
        diccionario = {}
        proyecto_actual = Proyecto.objects.get(id=request.POST['proyecto'])
        diccionario['proyecto']=proyecto_actual
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado

        lista_historias = Historia.objects.filter(proyecto=proyecto_actual, activo=True).order_by('nombre')
        diccionario['historias']=lista_historias

        if len(Rol.objects.filter(cerrar_proyecto = True, usuario= usuario_logueado, activo=True, proyecto=request.POST['proyecto'])): #Si el logueado es Scrum Master

            return render(request, self.template_name, diccionario)
        else:
            diccionario['error']= 'No posee el permiso'
            return render(request, super(FinalizarProyecto, self).template_name, diccionario)


class FinalizarProyectoConfirm(LoginRequiredMixin, ProyectoView):

    template_name = 'FinalizarProyectoConfirm.html'
    def post(self, request, *args, **kwargs):
        """
        Realiza la verifiacion de que el usuario posea el permiso y luego muestra la finalizacion de proyecto

        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: Retorna un mensaje de error, en el caso de que el usuario no posea permisos para finalizar o no se pueda
                Retorna la pagina donde se puede observar la finalizacion correcta

        """
        diccionario = {}
        proyecto_actual = Proyecto.objects.get(id=request.POST['proyecto'])
        diccionario['proyecto']=proyecto_actual
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado

        Historias = Historia.objects.filter(proyecto=proyecto_actual, activo=True)

        if not len(Historia.objects.filter(estado_scrum = 'Pendiente', proyecto=proyecto_actual, activo=True).all()) and not len(Sprint.objects.filter(estado='En Ejecucion', proyecto=proyecto_actual, activo=True).all()):
            proyecto_actual.estado = 'F'
            proyecto_actual.save()
            return render(request, self.template_name, diccionario)
        else:
            diccionario['error']= 'Algunas Historias aun no han sido finalizadas o algunos Sprints no han sido Ejecutados, no se puede finalizar'
            return render(request, self.template_name, diccionario)






