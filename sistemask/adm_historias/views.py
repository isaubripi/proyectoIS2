from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Historia
from adm_usuarios.models import Usuario
from adm_proyectos.models import Proyecto

# Create your views here.

class HistoriaView(TemplateView):
    '''

    '''

    template_name = 'Historia.html'

    def post(self, request, *args, **kwargs):
        '''

        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        diccionario = {}

        proyecto_actual = Proyecto.objects.get(id=request.POST['proyecto'])
        diccionario['proyecto'] = proyecto_actual
        lista = Historia.objects.filter(proyecto=proyecto_actual, activo=True)
        diccionario['lista'] = lista
        return render(request, self.template_name, diccionario)

class CrearHistoria(HistoriaView):
    '''

    '''

    template_name = 'CrearHistoria.html'

    def post(self, request, *args, **kwargs):
        '''

        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        diccionario = {}
        return render(request, self.template_name, diccionario)

class CrearHistoriaConfirm(CrearHistoria):
    '''

    '''

    template_name = 'CrearHistoriaConfirm.html'

    def post(self, request, *args, **kwargs):
        '''

        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        hu_nombre = request.POST['nombre_historia']
        #hu_proyecto = request.POST['proyecto']
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

        nueva_historia = Historia(nombre=hu_nombre, #proyecto=hu_proyecto,
                                  prioridad=hu_prioridad,
                                  val_negocio=hu_val_negocio, val_tecnico=hu_val_tecnico, size=hu_size,
                                  descripcion=hu_descripcion, codigo=hu_codigo, #acumulador=hu_acumulador, historial=hu_historial, flujo=hu_flujo, estado=hu_estado,
                                  activo=True)
        #nueva_historia.asignado.add(Usuario.objects.get(nombre=hu_asignado))
        nueva_historia.save()
        return render(request, self.template_name)


class EditarHistoria(TemplateView):
    '''

    '''

    template_name = 'EditarHistoria.html'

    def post(self, request, *args, **kwargs):
        '''

        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        diccionario = {}
        historia_actual = Historia.objects.get(id=request.POST['historia'])
        diccionario['historia'] = historia_actual
        return render (request, self.template_name, diccionario)

class EditarHistoriaConfirm(EditarHistoria):
    '''

    '''

    template_name = 'EditarHistoriaConfirm.html'

    def post(self, request, *args, **kwargs):
        '''

        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

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

        return render(request, self.template_name)

class EliminarHistoria(HistoriaView):
    '''

    '''

    template_name = 'EliminarHistoria.html'

    def post(self, request, *args, **kwargs):
        '''

        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        historia_eliminada = Historia.objects.get(id=request.POST['historia'])
        historia_eliminada.activo = False
        historia_eliminada.save()

        return render(request, self.template_name)