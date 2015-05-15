# -.- coding: utf-8 -.-
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Historia, Historial, Registro
from adm_usuarios.models import Usuario
from adm_proyectos.models import Proyecto
from adm_actividades.models import Actividad
from adm_proyectos.views import LoginRequiredMixin
from django.utils import timezone
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .forms import ArchivoAdjunto

# Create your views here.

class HistoriaView(TemplateView):
    '''
    Esta clase muestra las historias de un proyecto.
    Hereda de TeamplateView.
    '''

    template_name = 'Historia.html'

    def post(self, request, *args, **kwargs):
        '''
        Esta funcion tiene los parametros:
        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: el archivo html y el diccionario
        '''

        diccionario = {}

        proyecto_actual = Proyecto.objects.get(id=request.POST['proyecto'])
        diccionario['proyecto'] = proyecto_actual
        lista = Historia.objects.filter(proyecto=proyecto_actual, activo=True)
        diccionario['lista'] = lista
        diccionario['logueado']= Usuario.objects.get(id=request.POST['login'])
        return render(request, self.template_name, diccionario)

class HistoriaNView(HistoriaView):
    '''
    Esta clase muestra una historia especifica de un proyecto y las opciones de actualizacion de la misma.
    Hereda de HistoriaView.
    '''

    template_name = 'HistoriaN.html'

    def post(self, request, *args, **kwargs):
        '''
        Esta funcion tiene los parametros:
        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: el archivo html y el diccionario
        '''

        diccionario = {}

        proyecto_actual = Proyecto.objects.get(id=request.POST['proyecto'])
        diccionario['proyecto'] = proyecto_actual
        diccionario['logueado']= Usuario.objects.get(id=request.POST['login'])
        historia_actual = Historia.objects.get(id=request.POST['historia'])
        diccionario['historia'] = historia_actual
        return render(request, self.template_name, diccionario)



class CrearHistoria(LoginRequiredMixin, HistoriaView):
    '''
    Esta clase crea una historia nueva en un proyecto.
    Hereda de LoginRequiredMixin y de HistoriaView
    '''

    template_name = 'CrearHistoria.html'

    def post(self, request, *args, **kwargs):
        '''
        Esta funcion tiene los parametros:
        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: el archivo html y el diccionario
        '''

        diccionario = {}

        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        proyecto_actual = Proyecto.objects.get(id=request.POST['proyecto'])
        diccionario['proyecto'] = proyecto_actual
        return render(request, self.template_name, diccionario)

class CrearHistoriaConfirm(CrearHistoria):
    '''
    Esta clase confirma la creacion de una historia en un proyecto.
    Hereda de CrearHistoria
    '''

    template_name = 'CrearHistoriaConfirm.html'

    def post(self, request, *args, **kwargs):
        '''
        Esta funcion tiene los parametros:
        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return:request, html y diccionario
        '''
        diccionario = {}
        usuario_logueado = Usuario.objects.get(id= request.POST['login'])
        proyecto_actual = Proyecto.objects.get(id= request.POST['proyecto_historia'])
        diccionario['logueado'] = usuario_logueado
        diccionario['proyecto'] = proyecto_actual


        hu_nombre = request.POST['nombre_historia']
        hu_proyecto = request.POST['proyecto_historia']
        hu_prioridad = request.POST['prioridad_historia']
        hu_val_negocio = request.POST['negocio_historia']
        hu_val_tecnico = request.POST['tecnico_historia']
        hu_size = request.POST['size_historia']
        hu_descripcion = request.POST['descripcion_historia']
        hu_codigo = request.POST['codigo_historia']
        #hu_acumulador = request.POST['acumulador_historia']
        #hu_historial = request.POST['historial_historia']
        #hu_asignado = request.POST['asignado_historia']
        #hu_flujo = request.POST['flujo_historia']
        #hu_estado = request.POST['estado_historia']
        #archivo = models.FilePathField
        #sprint = models.ForeignKey(Sprint, null=True)


        if len(Historia.objects.filter(nombre=hu_nombre, proyecto=hu_proyecto, activo=True)):
            error_nombre = 'Nombre de historia ya exite. Intente otro'
            diccionario['error'] = error_nombre
            return render(request, super(CrearHistoriaConfirm, self).template_name, diccionario)

        if len(Historia.objects.filter(codigo=hu_codigo, proyecto=hu_proyecto, activo=True)):
            error_codigo = 'Codigo de historia ya existe. Intente otro'
            diccionario['error'] = error_codigo
            return render(request, super(CrearHistoriaConfirm, self).template_name, diccionario)

        nueva_historia = Historia(nombre=hu_nombre, proyecto=Proyecto.objects.get(id=request.POST['proyecto_historia']),
                                  prioridad=hu_prioridad,
                                  val_negocio=hu_val_negocio, val_tecnico=hu_val_tecnico, size=hu_size,
                                  descripcion=hu_descripcion, codigo=hu_codigo, #acumulador=hu_acumulador, historial=hu_historial, flujo=hu_flujo, estado=hu_estado,
                                  activo=True)
        nueva_historia.estado = 'To Do'
        nueva_historia.save()
        historial = Historial.objects.create(id_historia = Historia.objects.get(nombre=hu_nombre, activo=True ),
                                             nombre=hu_nombre, proyecto=Proyecto.objects.get(id=request.POST['proyecto_historia']),
                                             prioridad=hu_prioridad, val_negocio=hu_val_negocio,
                                             val_tecnico=hu_val_tecnico, size=hu_size, estado='To Do',
                                             descripcion=hu_descripcion, codigo=hu_codigo, activo=True)

        historial.fecha = timezone.now()
        historial.save()
        diccionario['proyecto'] = Proyecto.objects.get(id=hu_proyecto)
        return render(request, self.template_name, diccionario)


class EditarHistoria(LoginRequiredMixin, HistoriaNView):
    '''
    Esta clase modifica una historia en un proyecto.
    Hereda de LoginRequiredMixin y de HistoriaView
    '''

    template_name = 'EditarHistoria.html'

    def post(self, request, *args, **kwargs):
        '''
        Esta funcion tiene los parametros:
        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: el archivo html y el diccionario
        '''
        diccionario = {}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado

        proyecto_actual = Proyecto.objects.get(id=request.POST['proyecto'])
        diccionario['proyecto'] = proyecto_actual
        historia_actual = Historia.objects.get(id=request.POST['historia'])
        diccionario['historia'] = historia_actual
        return render (request, self.template_name, diccionario)

class EditarHistoriaConfirm(EditarHistoria):
    '''
    Esta clase confirma la modificacion de una historia en un proyecto.
    Hereda de EditarHistoria
    '''

    template_name = 'EditarHistoriaConfirm.html'

    def post(self, request, *args, **kwargs):
        '''
        Esta funcion tiene los parametros:
        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: el archivo html y el diccionario
        '''
        diccionario = {}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        proyecto_actual = Proyecto.objects.get(id = request.POST['proyecto'])
        diccionario['proyecto'] = proyecto_actual

        historia_editada = Historia.objects.get(id=request.POST['historia'])
        nuevo_nombre = request.POST['nuevo_nombre']

        existe = Historia.objects.filter(nombre=nuevo_nombre, activo=True)

        if len(existe) and existe[0] != historia_editada:
            error_nombre = 'Nombre de historia ya existe. Intente otro'
            diccionario['error'] = error_nombre
            return render(request, super(EditarHistoriaConfirm, self).template_name, diccionario)

        nuevo_prioridad = request.POST['nuevo_prioridad']
        nuevo_negocio = request.POST['nuevo_negocio']
        nuevo_tecnico = request.POST['nuevo_tecnico']
        nuevo_size = request.POST['nuevo_size']
        nuevo_descripcion = request.POST['nuevo_descripcion']

        historia_editada.nombre = nuevo_nombre
        historia_editada.prioridad = nuevo_prioridad
        historia_editada.val_negocio = nuevo_negocio
        historia_editada.val_tecnico = nuevo_tecnico
        historia_editada.size = nuevo_size
        historia_editada.descripcion = nuevo_descripcion
        historia_editada.save()

        diccionario['historia'] = historia_editada

        historial = Historial.objects.create(id_historia = Historia.objects.get(nombre=nuevo_nombre, activo=True),
                                             nombre=nuevo_nombre, proyecto=Proyecto.objects.get(id=request.POST['proyecto']),
                                             prioridad=nuevo_prioridad, val_negocio=nuevo_negocio, val_tecnico=nuevo_tecnico, size=nuevo_size,
                                             descripcion=nuevo_descripcion, codigo=historia_editada.codigo, acumulador=historia_editada.acumulador,
                                             asignado=historia_editada.asignado, flujo=historia_editada.flujo, estado=historia_editada.estado,
                                             sprint=historia_editada.sprint, asignado_p=historia_editada.asignado_p, activo=True)
        historial.fecha = timezone.now()
        historial.save()
        return render(request, self.template_name, diccionario)

class EliminarHistoria(LoginRequiredMixin, HistoriaView):
    '''
    Esta clase elimina logicamente una historia de un proyecto. Pone en estado inactivo a la historia.
    Hereda de LoginRequiredMixin y de HistoriaView.
    '''

    template_name = 'EliminarHistoria.html'

    def post(self, request, *args, **kwargs):
        '''
        Esta funcion tiene los parametros:
        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: el archivo html y el diccionario
        '''
        diccionario = {}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        proyecto_actual = Proyecto.objects.get(id=request.POST['proyecto'])
        diccionario['proyecto'] = proyecto_actual
        historia_eliminada = Historia.objects.get(id=request.POST['historia'])
        historia_eliminada.activo = False
        historia_eliminada.save()

        historial = Historial.objects.create(id_historia=historia_eliminada, nombre=historia_eliminada.nombre, proyecto=proyecto_actual,
                                             prioridad=historia_eliminada.prioridad, val_negocio=historia_eliminada.val_negocio,
                                             val_tecnico=historia_eliminada.val_tecnico, size=historia_eliminada.size,
                                             descripcion=historia_eliminada.descripcion,
                                             codigo=historia_eliminada.codigo, acumulador=historia_eliminada.acumulador,
                                             asignado=historia_eliminada.asignado, flujo=historia_eliminada.flujo,
                                             estado=historia_eliminada.estado, sprint=historia_eliminada.sprint,
                                             asignado_p=historia_eliminada.asignado_p, activo=False)
        historial.fecha = timezone.now()
        historial.save()

        return render(request, self.template_name, diccionario)


class VerHistorial(LoginRequiredMixin, HistoriaNView):
    '''
    Esta clase permite ver el historial de una historia de usuario de un proyecto.
    Hereda de LoginRequiredMixin y de HistoriaView.
    '''

    template_name = 'VerHistorial.html'

    def post(self, request, *args, **kwargs):
        '''
        Esta funcion tiene los parametros:
        :param request:
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: el archivo html y el diccionario
        '''

        diccionario = {}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        proyecto_actual = Proyecto.objects.get(id=request.POST['proyecto'])
        diccionario['proyecto'] = proyecto_actual
        historia_actual = Historia.objects.get(id=request.POST['historia'])
        lista = Historial.objects.filter(id_historia=request.POST['historia'])
        diccionario['lista'] = lista
        diccionario['historia_actual'] = historia_actual

        return render(request, self.template_name, diccionario)


class CargarHoras(LoginRequiredMixin, HistoriaNView):
    '''
    Esta clase permite cargar las horas que se trabajo en una tarea de una historia de usuario en un proyecto,
    describir brevemente la tarea, poner un nombre a la tarea realizada.
    Hereda de LoginRequiredMixin y de HistoriaView.
    '''

    template_name = 'CargarHoras.html'

    def post(self, request, *args, **kwargs):
        '''
        Esta funcion tiene los parametros:
        :param request:
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: request, html y diccionario
        '''
        diccionario = {}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        proyecto_actual = Proyecto.objects.get(id=request.POST['proyecto'])
        diccionario['proyecto'] = proyecto_actual
        historia_actual = Historia.objects.get(id=request.POST['historia'])
        diccionario['historia'] = historia_actual
        return render(request, self.template_name, diccionario)

class CargarHorasConfirm(CargarHoras):
    '''
    Esta clase confirma la carga de horas trabajadas sobre una historia de usuario en proyecto, confirma
    la descripcion y el nombre de la tarea realizada.
    Hereda de CargarHoras
    '''

    template_name = 'CargarHorasConfirm.html'

    def post(self, request, *args, **kwargs):
        '''
        Esta funcion tiene los parametros:
        :param request:
        :param args: Para mapear los argumentos posicionales a la tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: el archivo html y el diccionario
        '''
        diccionario = {}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        proyecto_actual = Proyecto.objects.get(id = request.POST['proyecto'])
        diccionario['proyecto'] = proyecto_actual

        historia = Historia.objects.get(id=request.POST['historia'])
        horas = 0
        horas = request.POST['horas']

        historia.acumulador = historia.acumulador + int(horas)



        diccionario['historia'] = historia

        registros = Registro.objects.filter(id_historia=historia, activo=True)
        ord = 1
        for i in registros:
            ord += 1

        nombre_tarea = request.POST['nombre_tarea']
        descripcion_tarea = request.POST['descripcion_tarea']
        diccionario['descripcion_tarea'] = descripcion_tarea

        for registro in registros:
            if  nombre_tarea == registro.nombre:
                diccionario['error'] = "Nombre de tarea ya existe. Intente otro."
                return render(request, super(CargarHorasConfirm, self).template_name, diccionario)


        registro_nuevo = Registro.objects.create(id_historia=historia, orden=ord, nombre=nombre_tarea,
                                                 proyecto=proyecto_actual, descripcion=descripcion_tarea,
                                                 horas=int(horas), fecha=timezone.now(), activo=True)
        if 'adjuntar' in request.POST:
            registro_nuevo.archivo = request.FILES['adjunto']

        registro_nuevo.save()
        historia.save()

        historial = Historial.objects.create(id_historia=historia, nombre=historia.nombre, proyecto=proyecto_actual,
                                             prioridad=historia.prioridad, val_negocio=historia.val_negocio,
                                             val_tecnico=historia.val_tecnico, size=historia.size,
                                             descripcion=historia.descripcion,
                                             codigo=historia.codigo, acumulador=historia.acumulador,
                                             asignado=historia.asignado, flujo=historia.flujo,
                                             estado=historia.estado, sprint=historia.sprint,
                                             asignado_p=historia.asignado_p, activo=False)
        historial.fecha = timezone.now()
        historial.save()

        email_context = {
            'titulo': 'Registro Tarea: ' + nombre_tarea,
            'usuario': usuario_logueado.nombre,
            'mensaje': 'Se ha registrado una nueva tarea. Los detalles de la tarea son:\n'
                            + '\nNOMBRE: ' + nombre_tarea
                            + '\nNUMERO: ' + str(ord)
                            + '\nHISTORIA: ' + historia.nombre
                            + '\nDESARROLLADOR: ' + usuario_logueado.nombre
                            + '\nPROYECTO: ' + proyecto_actual.nombre
                            + '\nDESCRIPCION: ' + descripcion_tarea
                            + '\nHORAS EMPLEADAS: ' + horas
                            + '\nFLUJO: ' + historia.flujo.nombre,
        }
        # se renderiza el template con el context
        email_html = render_to_string('email.html', email_context)

        # se quitan las etiquetas html para que quede en texto plano
        email_text = strip_tags(email_html)

        correo = EmailMultiAlternatives(
            'Nueva tarea registrada en historia',  # Asunto
            email_text,  # contenido del correo
            'sistemaskmail@gmail.com',  # quien lo envía
            [usuario_logueado.email, proyecto_actual.scrum_master.email],  # a quien se envía
        )

        # se especifica que el contenido es html
        correo.attach(email_html, 'text/html')
        # se envía el correo
        correo.send()



        return render(request, self.template_name, diccionario)



class VerDetalles(LoginRequiredMixin, HistoriaNView):
    '''
    Esta clase permite ver los detalles de una historia de usuario de un proyecto.
    Hereda de LoginRequiredMixin y de HistoriaView.
    '''

    template_name = 'VerDetalles.html'

    def post(self, request, *args, **kwargs):
        '''
        Esta funcion tiene los siguientes parametros:
        :param request:
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: el arhivo html y el diccionario
        '''

        diccionario = {}

        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        proyecto_actual = Proyecto.objects.get(id=request.POST['proyecto'])
        diccionario['proyecto'] = proyecto_actual
        historia_actual = Historia.objects.get(id=request.POST['historia'])
        diccionario['historia'] = historia_actual
        return render(request, self.template_name, diccionario)


class VerTareas(LoginRequiredMixin, HistoriaNView):
    '''
    Esta clase permite ver las tareas que fueron realizadas y registradas de una historia de usuario.
    Hereda de LoginRequiredMixin y de HistoriaView.
    '''

    template_name = 'VerTareas.html'

    def post(self, request, *args, **kwargs):
        '''
        Esta funcion tiene los siguientes parametros:
        :param request:
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: el archivo html y el diccionario
        '''
        diccionario = {}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado

        proyecto_actual = Proyecto.objects.get(id=request.POST['proyecto'])
        diccionario['proyecto'] = proyecto_actual

        historia_actual = Historia.objects.get(id=request.POST['historia'])
        diccionario['historia'] = historia_actual

        lista = Registro.objects.filter(id_historia=historia_actual, activo=True)
        diccionario['registros'] = lista

        return render(request, self.template_name, diccionario)


class CambiarEstadoActividad(LoginRequiredMixin, HistoriaNView):
    '''
    Esta clase permite cambiar el estado de una historia de usuario.
    Hereda de LoginRequiredMixin y de HistoriaView.
    '''

    template_name = 'CambiarEstadoActividad.html'

    def post(self, request, *args, **kwargs):
        '''
        Esta funcion tiene los siguientes parametros:
        :param request:
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: el archivo html y el diccionario.
        '''

        diccionario = {}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado

        proyecto_actual = Proyecto.objects.get(id=request.POST['proyecto'])
        diccionario['proyecto'] = proyecto_actual

        historia_actual = Historia.objects.get(id=request.POST['historia'])
        diccionario['historia'] = historia_actual

        secuencia_actividad_siguiente = historia_actual.actividad.secuencia + 1
        diccionario['secuencia'] = secuencia_actividad_siguiente

        actividades = Actividad.objects.filter(flujo=historia_actual.flujo.id).order_by('secuencia')
        diccionario['actividades'] = actividades

        return render(request, self.template_name, diccionario)

class CambiarEstadoActividadConfirm(CambiarEstadoActividad):
    '''
    Esta clase confirma el cambio de estado de una historia de usuario.
    Hereda de CambiarEstadoActividad.
    '''

    template_name = 'CambiarEstadoActividadConfirm.html'

    def post(self, request, *args, **kwargs):
        '''
        Esta funcion tiene los siguientes parametros:
        :param request: Peticion web
        :param args: Para mapear los argumentos posicionales a al tupla
        :param kwargs: Diccionario para mapear los argumentos de palabra clave
        :return: el archivo html y el diccionario
        '''

        diccionario = {}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado

        proyecto_actual = Proyecto.objects.get(id=request.POST['proyecto'])
        diccionario['proyecto'] = proyecto_actual

        historia = Historia.objects.get(id=request.POST['historia'])

        historia.estado = request.POST['estado']
        historia.actividad = Actividad.objects.get(id=request.POST['actividad'])
        historia.save()
        diccionario['historia'] = historia
        historial = Historial.objects.create(id_historia=historia, nombre=historia.nombre, proyecto=proyecto_actual,
                                             prioridad=historia.prioridad, val_negocio=historia.val_negocio,
                                             val_tecnico=historia.val_tecnico, size=historia.size,
                                             descripcion=historia.descripcion,
                                             codigo=historia.codigo, acumulador=historia.acumulador,
                                             asignado=historia.asignado, flujo=historia.flujo,
                                             estado=historia.estado, actividad=historia.actividad.nombre,
                                             sprint=historia.sprint,
                                             asignado_p=historia.asignado_p, activo=False)
        historial.fecha = timezone.now()
        historial.save()


        return render(request, self.template_name, diccionario)