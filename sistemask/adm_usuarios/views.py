# coding=utf-8

from django.http import request
from django.views.generic import TemplateView
from adm_usuarios.models import Usuario

from django.shortcuts import render

#La clase inicio es el que maneja el Menu Principal
class inicio(TemplateView):
    """Esta clase se encarga de realizar la autenticacion de usuarios"""

    def post(self, request, *args, **kwargs):
        """Este metodo se encarga de verificar el usuario y la
        contrasenha para luego enviar la pagina de inicio"""                #En el metodo post en la condicion if
        if 'user' in request.POST:                                      #preguntamos si la pagina desde donde se lo
            buscar_user = request.POST['user']                          #llamo es el login:
            buscar_password = request.POST['pass']                      #Verifica el nombre de usuario y la
            error= ""                                                   #contrasenha ingresadas para verificar
            for i in Usuario.objects.all():                            #si existe la entrada en la BD Usuarios
                if i.estado:
                    if i.username == buscar_user:
                        if i.password == buscar_password:
                            return render(request, 'inicio.html')
                        error= "Password incorrecto"
                        return render(request, 'login.html', {'error':error})
            error= "Usuario incorrecto"
            return render(request, 'login.html', {'error': error})
        else:                                                           #Si no se trata de la pagina de login quien
            return render(request, 'inicio.html')                       #lo llamo? Entonces no verifica absolutamente
                                                                        #nada y muestra la pagina solicitada

#La clase RegistrarUsuario se encarga de crear un nuevo usuario
class RegistrarUsuario(TemplateView):
    """Clase para lazar el formulario de creacion"""
    def post(self, request, *args, **kwargs):
        """retorna el formulario para la creacion"""                    #Devuelve la pagina en donde se encuentra el
        return render(request, 'CrearUsuario.html')                     #formulario

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

        if 'user' in request.POST:                                     #La pagina quien lo llama es CrearUsuario.html?
            new_user= request.POST['user']
                                                                    #Comprueba absolutamente todos los datos
            new_nombre= request.POST['nombre']                          #ingresados para averiguar si no se trata de
            new_apellido= request.POST['apellido']                      #un dato vacio el cual genera problemas al
            new_email= request.POST['email']                            #intentar guardar en la BD
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
            return render(request, 'EditarUsuario.html', {'usuario':modificacion})




'''def adm_usuarios_inicio(request):
    u = User.objects.all().order_by('-id')
    return render_to_response('adm_usuarios_inicio.html',{"u": u}, context_instance=RequestContext(request))'''



'''def register_view(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['username']
            nombre = form.cleaned_data['first_name']
            apellido = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password_one = form.cleaned_data['password_one']
            password_two = form.cleaned_data['password_two']
            u = User(username = usuario,email=email,password= password_one,first_name= nombre, last_name= apellido )
            u.save() #Guardar el objeto
            return render_to_response('registro_exito.html',context_instance= RequestContext(request))
        else:
            ctx = {'form': form}
            return render_to_response('registro.html', ctx, context_instance= RequestContext(request))
    ctx = {'form': form}
    return render_to_response('registro.html', ctx, context_instance= RequestContext(request))


def editar_usuario(request, id):
    u = User.objects.get(id=id)
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['username']
            nombre = form.cleaned_data['first_name']
            apellido = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password_one = form.cleaned_data['password_one']
            password_two = form.cleaned_data['password_two']
            u = User(username = usuario,email=email,password= password_one,first_name= nombre, last_name= apellido )
            u.save() #Guardar el objeto
    if request.method == "GET":
        form = RegisterForm(initial={
            'usuario' : u.username,
            'nombre' : u.first_name,
            'apellido' : u.last_name,
            'email' : u.email,
            'password_one' : u.password,
            #'password_two' : u.password_two,

        })
    ctx = {'form':form,User:u}

    return render_to_response('editar_usuario.html', ctx, context_instance= RequestContext(request))'''