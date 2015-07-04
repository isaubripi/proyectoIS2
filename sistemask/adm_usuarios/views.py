# coding=utf-8

from django.shortcuts import render
from adm_proyectos.views import ProyectoView
from .models import Usuario
from adm_roles.models import Rol
from adm_proyectos.models import Proyecto
from django.views.generic import TemplateView

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from adm_proyectos.views import LoginRequiredMixin

from django.utils import timezone
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Create your views here.
#Lista de usuarios
class UsuarioView(ProyectoView):
    template_name = 'Usuario.html'
    context_object_name = 'lista_usuarios'

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        #Solamente el Administrador del Sistema puede ingresar a la Administracion de Usuarios
        if len(Rol.objects.filter(crear_usuario = True , usuario= usuario_logueado)):
            diccionario[self.context_object_name]= Usuario.objects.filter(estado=True)
            return render(request, self.template_name, diccionario)
        else:
            diccionario['error']= 'No posee permisos para ver los usuarios del sistema'
            diccionario[super(UsuarioView, self).context_object_name]= Proyecto.objects.filter(activo= True)
            return render(request, super(UsuarioView, self).template_name, diccionario)

#Creacion de usuario
class CrearUsuario(LoginRequiredMixin, UsuarioView):
    template_name = 'CrearUsuario.html'
    context_object_name = 'lista_usuarios'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        if len(Rol.objects.filter(crear_usuario=True, usuario= usuario_logueado)):
            return render(request, self.template_name, diccionario)
        else:
            diccionario['error']= 'No posee permiso para crear usuario'
            diccionario[self.context_object_name]= Usuario.objects.filter(estado=True)
            return render(request, super(CrearUsuario, self).template_name, diccionario)


class CrearUsuarioConfirm(CrearUsuario):
    template_name = 'CrearUsuarioConfirm.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        nuevo_nick= request.POST['user']
        existe= Usuario.objects.filter(username= nuevo_nick)
        if len(existe):
            diccionario['error']= 'El nombre de usuario ya existe'
            return render(request, super(CrearUsuarioConfirm, self).template_name, diccionario)
        nuevo_usuario= Usuario()
        nuevo_usuario.username= nuevo_nick
        nuevo_usuario.password= request.POST['pass']
        nuevo_usuario.nombre= request.POST['nombre']
        nuevo_usuario.apellido= request.POST['apellido']
        nuevo_usuario.cedula= request.POST['cedula']
        nuevo_usuario.email= request.POST['email']
        nuevo_usuario.save()
        nuevo_user= User()
        nuevo_user.username = nuevo_nick
        password = request.POST['pass']
        nuevo_user.set_password(password)
        nuevo_user.first_name = request.POST['nombre']
        nuevo_user.last_name = request.POST['apellido']
        nuevo_user.email = request.POST['email']
        nuevo_user.is_active = True
        nuevo_user.save()
        return render(request, self.template_name, diccionario)

class EditarUsuario(LoginRequiredMixin, UsuarioView):
    template_name = 'EditarUsuario.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        diccionario['usuario']= Usuario.objects.get(id= request.POST['codigo'])
        return render(request, self.template_name, diccionario)

class EditarUsuarioConfirm(EditarUsuario):
    template_name = 'EditarUsuarioConfirm.html'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        modificacion= Usuario.objects.get(id= request.POST['codigo'])
        modificacion_nick= request.POST['user']
        username_old = modificacion.username
        modificacion_user = User.objects.get(username=username_old)
        existe= Usuario.objects.filter(username= modificacion_nick)
        if len(existe) and existe[0]!=modificacion:
            diccionario['error']= 'El nombre de usuario ya existe'
            diccionario['usuario']= modificacion
            return render(request, super(EditarUsuarioConfirm, self).template_name, diccionario)
        modificacion.username= modificacion_nick
        modificacion.password= request.POST['pass']
        modificacion.nombre= request.POST['nombre']
        modificacion.apellido= request.POST['apellido']
        modificacion.cedula= request.POST['cedula']
        modificacion.email= request.POST['email']
        modificacion.save()

        #modificacion del model user

        modificacion_nick_user = request.POST['user']
        modificacion_user.username= modificacion_nick_user
        password = request.POST['pass']
        modificacion_user.set_password(password)
        modificacion_user.first_name= request.POST['nombre']
        modificacion_user.last_name= request.POST['apellido']
        modificacion_user.email= request.POST['email']
        modificacion_user.save()
        return render(request, self.template_name, diccionario)

class EliminarUsuario(LoginRequiredMixin, UsuarioView):
    template_name = 'EliminarUsuario.html'
    context_object_name = 'lista_usuarios'
    def post(self, request, *args, **kwargs):
        diccionario={}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        eliminado= Usuario.objects.get(id= request.POST['codigo'])
        delete = eliminado.username
        eliminado_user = User.objects.get(username=delete)

        #Verificar si es Administrador del Sistema
        if len(Rol.objects.filter(eliminar_usuario=True, usuario= usuario_logueado)):
            if len(Rol.objects.filter(nombre='Scrum Master', usuario= eliminado)):
                diccionario['lista_usuarios']= Usuario.objects.filter(estado= True)
                diccionario['error']= 'No se puede eliminar - El usuario es Scrum Master'
                return render(request, super(EliminarUsuario, self).template_name, diccionario)
            #Verificar si es scrum master de algun proyecto
            if len(Rol.objects.filter(nombre= 'Scrum_Master', usuario= eliminado, activo= True)):
                diccionario['lista_usuarios']= Usuario.objects.filter(estado= True)
                diccionario['error']= 'No se puede eliminar - El usuario es Scrum Master de un proyecto activo'
                return render(request, super(EliminarUsuario, self).template_name, diccionario)
            eliminado.estado= False
            eliminado.save()
            eliminado_user.is_active=False
            eliminado_user.save()
            return render(request, self.template_name, diccionario)
        else:
            diccionario['error']= 'No posee permiso para eliminar usuario'
            diccionario[self.context_object_name]= Usuario.objects.filter(estado=True)
            return render(request, super(EliminarUsuario, self).template_name, diccionario)


class AsignarRoles(LoginRequiredMixin, UsuarioView):
    template_name = 'AsignarRoles.html'
    def post(self, request, *args, **kwargs):
        diccionario = {}
        usuario_logueado = Usuario.objects.get(id = request.POST['login'])
        diccionario['logueado'] = usuario_logueado
        usuario_actual = Usuario.objects.get(id = request.POST['usuario'])
        diccionario['usuario_actual'] = usuario_actual
        #lista = usuario_actual.roles.all()
        lista = usuario_actual.roles.filter(proyecto= '', activo=True)
        diccionario['roles_asignados'] = lista
        #lista1 = Rol.objects.exclude(usuario=usuario_actual)
        lista1 = Rol.objects.filter(proyecto= '', activo=True)
        diccionario['no_asignados'] = lista1
        return render(request, self.template_name, diccionario)


class AsignarRolesConfirm(AsignarRoles):
    template_name = 'AsignarRolesConfirm.html'
    def post(self, request, *args, **kwargs):
        diccionario = {}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        usuario_actual = Usuario.objects.get(id = request.POST['user'])
        lista2 = usuario_actual.roles.all()
        lista3 = Rol.objects.exclude(usuario=usuario_actual)
        for rol in lista2:
            if rol.proyecto == '' and rol.nombre not in request.POST:
                usuario_actual.roles.remove(rol)
        for r in lista3:
            if r.nombre in request.POST:
                usuario_actual.roles.add(r)
        usuario_actual.save()
        return render(request, self.template_name, diccionario)


class GestionarRol(AsignarRoles):
    template_name = 'GestionarRol.html'
    def post(self, request, *args, **kwargs):
        diccionario = {}
        usuario_logueado = Usuario.objects.get(id=request.POST['login'])
        diccionario['logueado'] = usuario_logueado
        roles_sistema = Rol.objects.filter(proyecto='', activo=True)
        diccionario['roles'] = roles_sistema
        return render(request, self.template_name, diccionario)


class CreaRol(AsignarRoles):
    template_name = 'CreaRol.html'
    def post(self, request, *args, **kwargs):
        diccionario = {}
        usuario_logueado = Usuario.objects.get(id=request.POST['login'])
        diccionario['logueado'] = usuario_logueado
        #usuario_actual = Usuario.objects.get(id=request.POST['user'])
        #diccionario['usuario_actual'] = usuario_actual
        return render(request, self.template_name, diccionario)

class CreaRolConfirm(CreaRol):
    template_name = 'CreaRolConfirm.html'
    def post(self, request, *args, **kwargs):
        diccionario = {}
        usuario_logueado = Usuario.objects.get(id=request.POST['login'])
        diccionario['logueado'] = usuario_logueado

        rol_nombre= request.POST['nombre_rol']
        nuevo_rol = Rol(nombre= rol_nombre)

        if len(Rol.objects.filter(nombre= rol_nombre, activo= True, proyecto='')):
            i = 1
            while len(Rol.objects.filter(nombre= rol_nombre + '(' + str(i) + ')', activo= True, proyecto='')):
                i+=1
            rol_nombre = rol_nombre + '(' + str(i) + ')'

        nuevo_rol.nombre = rol_nombre


        nuevo_rol.proyecto = ''

        if 'crear_proyecto' in request.POST: nuevo_rol.crear_proyecto= True
        else: nuevo_rol.crear_proyecto= False

        if 'crear_usuario' in request.POST: nuevo_rol.crear_usuario= True
        else: nuevo_rol.crear_usuario= False

        if 'modificar_usuario' in request.POST: nuevo_rol.modificar_usuario= True
        else: nuevo_rol.modificar_usuario= False

        if 'eliminar_usuario' in request.POST: nuevo_rol.eliminar_usuario= True
        else: nuevo_rol.eliminar_usuario= False

        if 'agregar_rol' in request.POST: nuevo_rol.agregar_rol= True
        else: nuevo_rol.agregar_rol= False

        if 'modificar_rol' in request.POST: nuevo_rol.modificar_rol= True
        else: nuevo_rol.modificar_rol= False

        if 'eliminar_rol' in request.POST: nuevo_rol.eliminar_rol= True
        else: nuevo_rol.eliminar_rol= False

        if 'asignar_usuario_inicial' in request.POST: nuevo_rol.asignar_usuario_inicial= True
        else: nuevo_rol.asignar_usuario_inicial= False

        if 'asignar_roles_usuario' in request.POST: nuevo_rol.asignar_roles_usuario= True
        else: nuevo_rol.asignar_roles_usuario= False

        nuevo_rol.activo= True

        nuevo_rol.save()
        return render(request, self.template_name, diccionario)


class EditaRol(GestionarRol):
    template_name = 'EditaRol.html'
    def post(self, request, *args, **kwargs):
        diccionario = {}
        usuario_logueado = Usuario.objects.get(id=request.POST['login'])
        diccionario['logueado'] = usuario_logueado
        #usuario_actual = Usuario.objects.get(id=request.POST['user'])
        #diccionario['usuario_actual'] = usuario_actual
        rol_editar = Rol.objects.get(id=request.POST['rol'])
        diccionario['rol'] = rol_editar
        if rol_editar.nombre== 'Administrador':
            diccionario['error']= 'Rol: Administrador - No se puede eliminar'

            return render(request, super(EditaRol, self).template_name, diccionario)
        return render(request, self.template_name, diccionario)

class EditaRolConfirm(EditaRol):
    template_name = 'EditaRolConfirm.html'
    def post(self, request, *args, **kwargs):
        diccionario = {}
        usuario_logueado = Usuario.objects.get(id=request.POST['login'])
        diccionario['logueado'] = usuario_logueado

        rol_editar = Rol.objects.get(id=request.POST['rol'])

        rol_nombre= request.POST['nombre_rol']


        rol_editar.nombre = rol_nombre

        rol_editar.proyecto = ''

        if 'crear_proyecto' in request.POST: rol_editar.crear_proyecto= True
        else: rol_editar.crear_proyecto= False

        if 'crear_usuario' in request.POST: rol_editar.crear_usuario= True
        else: rol_editar.crear_usuario= False

        if 'modificar_usuario' in request.POST: rol_editar.modificar_usuario= True
        else: rol_editar.modificar_usuario= False

        if 'eliminar_usuario' in request.POST: rol_editar.eliminar_usuario= True
        else: rol_editar.eliminar_usuario= False

        if 'agregar_rol' in request.POST: rol_editar.agregar_rol= True
        else: rol_editar.agregar_rol= False

        if 'modificar_rol' in request.POST: rol_editar.modificar_rol= True
        else: rol_editar.modificar_rol= False

        if 'eliminar_rol' in request.POST: rol_editar.eliminar_rol= True
        else: rol_editar.eliminar_rol= False

        if 'asignar_usuario_inicial' in request.POST: rol_editar.asignar_usuario_inicial= True
        else: rol_editar.asignar_usuario_inicial= False

        if 'asignar_roles_usuario' in request.POST: rol_editar.asignar_roles_usuario= True
        else: rol_editar.asignar_roles_usuario= False

        rol_editar.activo= True

        rol_editar.save()
        return render(request, self.template_name, diccionario)

class EliminaRol(GestionarRol):
    '''Esta clase elimina un rol, es decir, pone en estado inactivo el rol.
    El rol de Scrum Master no se puede eliminar.
    Hereda de RolView.
    template_name es el archivo html de esta funcion.

    '''
    template_name = 'EliminaRol.html'
    def post(self, request, *args, **kwargs):
        '''
        Esta funcion tiene los parametros:
        :param request:
        :param args:
        :param kwargs:
        :return: request, el archivo html y el diccionario.
        '''


        diccionario = {}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado

        rol_actual= Rol.objects.get(id= request.POST['rol'])

        if rol_actual.nombre== 'Administrador':
            diccionario['error']= 'Rol: Administrador - No se puede eliminar'

            return render(request, super(EliminaRol, self).template_name, diccionario)

        if len(Rol.objects.filter(id=rol_actual.id, activo=True, proyecto='', usuario=None)) != 0:
            rol_actual.activo = False
            rol_actual.save()
            return render(request, self.template_name, diccionario)
        else:
            diccionario['error']= 'El rol esta asignado, no se puede eliminar'

            return render(request, super(EliminaRol, self).template_name, diccionario)

        #roles= Rol.objects.filter(nombre= rol_actual.nombre, activo= True)
        #for rol_actual in roles:




'''from django.http import request
from django.views.generic import TemplateView
from adm_usuarios.models import Usuario

from django.shortcuts import render

#La clase inicio es el que maneja el Menu Principal
class inicio(TemplateView):
    """Esta clase se encarga de realizar la autenticacion de usuarios"""

    def post(self, request, *args, **kwargs):

        """Este metodo se encarga de verificar el usuario y la
        contrasenha para luego enviar la pagina de inicio"""

        diccionario = {}                                               #En el metodo post en la condicion if
        if 'user' in request.POST:                                      #preguntamos si la pagina desde donde se lo
            buscar_user = request.POST['user']                          #llamo es el login:
            buscar_password = request.POST['pass']                      #Verifica el nombre de usuario y la
            error= ""                                                   #contrasenha ingresadas para verificar
            for i in Usuario.objects.all():                            #si existe la entrada en la tabla Usuarios
                if i.estado:
                    if i.username == buscar_user:
                        if i.password == buscar_password:
                            diccionario['logueado']= i
                            return render(request, 'inicio.html', diccionario)
                        error= "Password incorrecto"
                        return render(request, 'login1.html', {'error':error})
            error= "Usuario incorrecto"
            return render(request, 'login1.html', {'error': error})
        else:                                                           #Si no se trata de la pagina de login quien
            return render(request, 'inicio.html', diccionario)                       #lo llamo? Entonces no verifica absolutamente
                                                                        #nada y muestra la pagina solicitada

#La clase RegistrarUsuario se encarga de crear un nuevo usuario
class RegistrarUsuario(TemplateView):
    """Clase para lazar el formulario de creacion"""
    #context_object_name = 'lista_usuarios'
    #template_name = CrearUsuario
    def post(self, request, *args, **kwargs):
        """
        retorna el formulario para la creacion
        """
        #diccionario={}
        #usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        #diccionario['logueado']= usuario_logueado                                          #Devuelve la pagina en donde se encuentra el
        return render(request, 'CrearUsuario.html')                                         #formulario

#La clase ListarUsuario se encarga de la vista principal de Administracion de Usuarios
class ListarUsuario(TemplateView):
    """Clase para controlar la creacion de usuarios"""
    def post(self, request, *args, **kwargs):
        """
        Este metodo se encarga de recibir los datos para la creacion
        de un usuario.
        Hace las verficaciones correspondientes para que no se permita repetir:
        - nombres de usuarios
        - cedula de identidad
        - correo electronico

        luego retorna la pantalla inicial de la administracion
        de usuarios
        """

        if 'user' in request.POST:                                     #La pagina quien lo llama es CrearUsuario.html
            new_user= request.POST['user']
                                                                    #Comprueba absolutamente todos los datos
            new_nombre= request.POST['nombre']                          #ingresados para averiguar si no se trata de
            new_apellido= request.POST['apellido']                      #un dato vacio el cual genera problemas al
            new_email= request.POST['email']                            #intentar guardar en la tabla correspondiente
            new_cedula= request.POST['cedula']
            new_password= request.POST['pass']


            existe = Usuario.objects.filter(username = new_user)
            existeb= Usuario.objects.filter(email= new_email)
            existec= Usuario.objects.filter(cedula= new_cedula)

            if len(existe) or len(existeb) or len(existec):

                if len(existe) and len(existeb) and len(existec):
                    error = "El nombre de usuario, email y cedula ya se encuentran registrados"

                elif len(existeb) and len(existec):
                    error = "El email y la cedula ya se encuentran registrados"

                elif len(existe) and len(existec):
                    error = "El nombre de usuario y la cedula ya se encuentran registrados"

                elif len(existe) and len(existeb):
                    error = "El nombre de usuario y el email ya se encuentran registrados"

                elif len(existec):
                    error= "El numero de cedula ya se encuentran registrados"

                elif len(existe):
                    error= "El nombre de usuario ya existe"

                elif len(existeb):
                    error= "La direccion de correo ya esta registrada"

                aux = Usuario(username= new_user, nombre= new_nombre, apellido= new_apellido, email= new_email, cedula= new_cedula, password= new_password)
                return render(request, 'CrearUsuario.html', {'usuario':aux, 'error': error})


            if new_user and new_nombre and new_apellido and new_email and new_password and new_cedula:
                nuevo_usuario= Usuario(username= new_user, nombre= new_nombre, apellido= new_apellido, email= new_email, cedula= new_cedula, password= new_password) #insert into values
                nuevo_usuario.save()                                    #guardamos en la base de datos
            else:
                error2 = "Debe introducir todos los datos requeridos"
                aux = Usuario(username= new_user, nombre= new_nombre, apellido= new_apellido, email= new_email, cedula= new_cedula, password= new_password)
                return render(request, 'CrearUsuario.html', {'usuario':aux, 'error2':error2})             #Si no logra grabar devuelve a la pagina anterior
        lista= Usuario.objects.all()
        return render(request, 'Usuario.html', {'lista_usuarios':lista})     #enviamos al html un diccionario que tiene par 'key':lista_de_Usuarios_Existentes



class eliminar(TemplateView):
    """Clase para mostrar la pagina de eliminacion"""
    def post(self, request, *args, **kwargs):
        """Retorna una pagina donde se confirma la eliminacion de un
        usuario"""
        return render(request, 'EliminarUsuario.html')


#La clase Cambio Estado se encarga de una pagina de confirmacion de cambios
class CambioEstado(TemplateView):
    """Clase para cambiar el estado de un usuario"""
    def post(self, request, *args, **kwargs):
        """
        Cambia el estado del usuario de activo a inactivo
        luego el usuario eliminado ya no se muestra
        en la lista de usuarios activos\
        """
        modif_codigo= request.POST['codigo']
        modificacion= Usuario.objects.get(id=modif_codigo)
        modificacion.estado= False
        modificacion.save()
        return render(request, 'CambioEstado.html')



#La clase Editar Usuario se encarga de la Edicion de Usuarios
class EditarUsuario(TemplateView):
    """
    Clase que muestra el formulario para la modificacion
    """
    def post(self, request, *args, **kwargs):
        """
        Se encarga de retornar la pagina con los
        datos cargados del usuario
        """
        modif_codigo= request.POST['codigo']
        modificacion= Usuario.objects.get(id= modif_codigo)
        return render(request, 'EditarUsuario.html', {'usuario':modificacion}) #Devuelve un formulario con lo campos
                                                                               #completados para modificar

#La clase EditarUsuarioConfirmar se encarga de una pagina de confirmacion de cambios
class EditarUsuarioConfirmar(TemplateView):
    """
    Verifica los cambios realizados y los valida
    """
    def post(self, request, *args, **kwargs): #Primero verifica si lo que le envio EditarUsuario.html son datos correctos

        """
        Se asegura que el momento de cambiar ciertos datos de los usuarios
        no se repitan datos como:
        * nombre de usuario
        * cedula de identidad
        * correo electronico

        luego realiza la actualizacion y vuelve
        a la pagina inicial de la administracion de usuarios
        """
        modif_codigo= request.POST['codigo']
        modificacion= Usuario.objects.get(id= modif_codigo)
        modificacion.username= request.POST['user']
        modificacion.nombre= request.POST['nombre']
        modificacion.apellido= request.POST['apellido']
        modificacion.cedula =request.POST['cedula']
        modificacion.email= request.POST['email']
        modificacion.password= request.POST['pass']

        existe = Usuario.objects.filter(username = modificacion.username)
        existeb= Usuario.objects.filter(email= modificacion.email)
        existec= Usuario.objects.filter(cedula= modificacion.cedula)

        error = ''
        if len(existe) or len(existeb) or len(existec):

            if len(existe) and len(existeb) and len(existec) and existe[0]!= modificacion and existeb[0]!= modificacion and existec[0]!= modificacion:
                error = "El nombre de usuario, email y cedula ya se encuentran registrados"

            elif len(existeb) and len(existec) and existeb[0]!=modificacion and existec[0]!= modificacion:
                error = "El email y la cedula ya se encuentran registrados"

            elif len(existe) and len(existec) and existe[0]!=modificacion and existec[0]!= modificacion:
                error = "El nombre de usuario y la cedula ya se encuentran registrados"

            elif len(existe) and len(existeb) and existe[0]!=modificacion and existeb[0]!= modificacion:
                error = "El nombre de usuario y el email ya se encuentran registrados"

            elif len(existec) and existec[0]!=modificacion:
                error= "El numero de cedula ya se encuentra registrados"

            elif len(existe) and existe[0]!=modificacion:
                error= "El nombre de usuario ya existe"

            elif len(existeb) and existeb[0]!=modificacion:
                error= "La direccion de correo ya esta registrada"

            if error != '':

                return render(request, 'EditarUsuario.html', {'usuario':modificacion, 'error': error})

        if modificacion.username and modificacion.nombre and modificacion.apellido and modificacion.email and modificacion.cedula and modificacion.password:
            modificacion.save()
            return render(request, 'EditarUsuarioConfirmar.html')
        else:
            return render(request, 'EditarUsuario.html', {'usuario':modificacion})'''

