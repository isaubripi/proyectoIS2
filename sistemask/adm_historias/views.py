from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Historia, Historial
from adm_usuarios.models import Usuario
from adm_proyectos.models import Proyecto
from adm_proyectos.views import LoginRequiredMixin
from django.utils import timezone

# Create your views here.

class HistoriaView(TemplateView):
    '''
    Esta clase muestra las historias de un proyecto.
    '''

    template_name = 'Historia.html'

    def post(self, request, *args, **kwargs):
        '''
        Esta funcion tiene los parametros:
        :param request:
        :param args:
        :param kwargs:
        :return: request, html y diccionario
        '''

        diccionario = {}

        proyecto_actual = Proyecto.objects.get(id=request.POST['proyecto'])
        diccionario['proyecto'] = proyecto_actual
        lista = Historia.objects.filter(proyecto=proyecto_actual, activo=True)
        diccionario['lista'] = lista
        diccionario['logueado']= Usuario.objects.get(id=request.POST['login'])
        return render(request, self.template_name, diccionario)

class CrearHistoria(LoginRequiredMixin, HistoriaView):
    '''
    Esta clase crea una historia nueva en un proyecto.
    '''

    template_name = 'CrearHistoria.html'

    def post(self, request, *args, **kwargs):
        '''
        Esta funcion tiene los parametros:
        :param request:
        :param args:
        :param kwargs:
        :return: request, html y diccionario
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
    '''

    template_name = 'CrearHistoriaConfirm.html'

    def post(self, request, *args, **kwargs):
        '''
        Esta funcion tiene los parametros:
        :param request:
        :param args:
        :param kwargs:
        :return:request, html y diccionario
        '''
        diccionario = {}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado


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


        if len(Historia.objects.filter(nombre=hu_nombre, activo=True)):
            error_nombre = 'Nombre de historia ya exite. Intente otro'
            return render(request, super(CrearHistoriaConfirm, self).template_name, {'error':error_nombre})

        if len(Historia.objects.filter(codigo=hu_codigo , activo=True)):
            error_codigo = 'Codigo de historia ya existe. Intente otro'
            return render(request, super(CrearHistoriaConfirm, self).template_name, {'error':error_codigo})

        nueva_historia = Historia(nombre=hu_nombre, proyecto=Proyecto.objects.get(id=request.POST['proyecto_historia']),
                                  prioridad=hu_prioridad,
                                  val_negocio=hu_val_negocio, val_tecnico=hu_val_tecnico, size=hu_size,
                                  descripcion=hu_descripcion, codigo=hu_codigo, #acumulador=hu_acumulador, historial=hu_historial, flujo=hu_flujo, estado=hu_estado,
                                  activo=True)
        #nueva_historia.asignado.add(Usuario.objects.get(nombre=hu_asignado))
        nueva_historia.save()
        historial = Historial.objects.create(id_historia = Historia.objects.get(nombre=hu_nombre),
                                             nombre=hu_nombre, proyecto=Proyecto.objects.get(id=request.POST['proyecto_historia']),
                                             prioridad=hu_prioridad, val_negocio=hu_val_negocio,
                                             val_tecnico=hu_val_tecnico, size=hu_size,
                                             descripcion=hu_descripcion, codigo=hu_codigo, activo=True)

        historial.fecha = timezone.now()
        historial.save()
        diccionario['proyecto'] = Proyecto.objects.get(id=hu_proyecto)
        return render(request, self.template_name, diccionario)


class EditarHistoria(LoginRequiredMixin, TemplateView):
    '''
    Esta clase modifica una historia en un proyecto.
    '''

    template_name = 'EditarHistoria.html'

    def post(self, request, *args, **kwargs):
        '''
        Esta funcion tiene los parametros:
        :param request:
        :param args:
        :param kwargs:
        :return: request, html y diccionario
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
    Esta clase confirma la modificacion de una historia en un proyecto:
    '''

    template_name = 'EditarHistoriaConfirm.html'

    def post(self, request, *args, **kwargs):
        '''
        Esta funcion tiene los parametros:
        :param request:
        :param args:
        :param kwargs:
        :return: request, html y diccionario
        '''
        diccionario = {}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        proyecto_actual = Proyecto.objects.get(id = request.POST['proyecto'])
        diccionario['proyecto'] = proyecto_actual

        historia_editada = Historia.objects.get(id=request.POST['historia'])
        nuevo_nombre = request.POST['nuevo_nombre']

        """if len(Historia.objects.filter(nombre=nuevo_nombre, activo=True)):
            error_nombre = 'Nombre de historia ya existe. Intente otro'
            return render(request, super(EditarHistoriaConfirm, self).template_name, {'error':error_nombre})"""

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

        historial = Historial.objects.create(id_historia = Historia.objects.get(nombre=nuevo_nombre),
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
    '''

    template_name = 'EliminarHistoria.html'

    def post(self, request, *args, **kwargs):
        '''
        Esta funcion tiene los parametros:
        :param request:
        :param args:
        :param kwargs:
        :return: request, html y diccionario
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


class VerHistorial(LoginRequiredMixin, HistoriaView):
    '''
    Esta clase permite ver el historial de una historia de usuario de un proyecto.
    '''

    template_name = 'VerHistorial.html'

    def post(self, request, *args, **kwargs):
        '''
        Esta funcion tiene los parametros:
        :param request:
        :param args:
        :param kwargs:
        :return: request, html y diccionario
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


class CargarHoras(LoginRequiredMixin, HistoriaView):
    '''
    Esta clase permite cargar las horas que se trabajo sobre una historia de usuario en un proyecto.
    '''

    template_name = 'CargarHoras.html'

    def post(self, request, *args, **kwargs):
        '''
        Esta funcion tiene los parametros:
        :param request:
        :param args:
        :param kwargs:
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
    Esta clase confirma la carga de horas trabajadas sobre una historia de usuario en proyecto.
    '''

    template_name = 'CargarHorasConfirm.html'

    def post(self, request, *args, **kwargs):
        '''
        Esta funcion tiene los parametros:
        :param request:
        :param args:
        :param kwargs:
        :return: request, html y diccionario
        '''
        diccionario = {}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        proyecto_actual = Proyecto.objects.get(id = request.POST['proyecto'])
        diccionario['proyecto'] = proyecto_actual

        historia = Historia.objects.get(id=request.POST['historia'])
        horas = request.POST['horas']

        historia.acumulador += int(horas)

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

        return render(request, self.template_name, diccionario)


class AsignarFlujo(LoginRequiredMixin, HistoriaView):
    '''

    '''

    template_name = 'AsignarFlujo.html'

    def post(self, request, *args, **kwargs):
        '''

        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        diccionario = {}
        usuario_logueado= Usuario.objects.get(id= request.POST['login'])
        diccionario['logueado']= usuario_logueado
        proyecto_actual = Proyecto.objects.get(id = request.POST['proyecto'])
        diccionario['proyecto'] = proyecto_actual