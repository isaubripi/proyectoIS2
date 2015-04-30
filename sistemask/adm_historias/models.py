from django.db import models
from adm_usuarios.models import Usuario
from adm_flujos.models import Flujo
from adm_proyectos.models import Proyecto
from adm_actividades.models import Actividad

# Create your models here.

class Historia(models.Model):

    '''
    Esta clase define el modelo de historia de usuario.
    Los campos de este modelo son:
        nombre: nombre de la historia
        proyecto: indica el proyecto en que esta la historia
        prioridad: indica la prioridad de la historia
        val_negocio: indica el valor de negocio de la historia
        val_tecnico: inidica el valor tecnico de la historia
        size: indica el tiempo estimado en horas en terminar la historia
        descripcion: una descripcion de la historia
        codigo: es el codigo de la historia
        acumulador: indica las horas trabajadas sobre la historia
        asignado: indica el usuario encargado de trabajar sobre la historia
        flujo: indica el flujo en que esta la historia
        estado: indica el estado en la actividad de un flujo en que esta la historia
        archivo: registra un archivo referente a la historia
        sprint: indica el sprint en que esta la historia
        asignado_p: indica si la historia esta asignada a un sprint o no
        activo: indica si la historia esta eliminada (False) o no (True)

    '''

    nombre = models.CharField(max_length=20)
    proyecto = models.ForeignKey(Proyecto, null=True)
    prioridad = models.IntegerField(default=0)
    val_negocio = models.IntegerField(default=0)
    val_tecnico = models.IntegerField(default=0)
    size = models.IntegerField(default=0)
    descripcion = models.CharField(max_length=100)
    codigo = models.CharField(max_length=5)
    acumulador = models.IntegerField(default=0)
    asignado = models.ForeignKey(Usuario, null=True)
    flujo = models.ForeignKey(Flujo, null=True)
    estado = models.CharField(max_length=5)
    archivo = models.FileField(upload_to=generate_filename)
    actividad = models.ForeignKey(Actividad, null=True)
    sprint = models.CharField(max_length=20)
    asignado_p = models.BooleanField(default=False)
    activo = models.BooleanField(default=False)


    def __unicode__(self):
        return self.nombre



class Historial(models.Model):
    '''
    Esta clase define el modelo de historial de historia de usuario.
    Los campos de este modelo son:
        id_historia: es el identificador de la historia (clave foranea)
        nombre: nombre de la historia
        proyecto: indica el proyecto en que esta la historia
        prioridad: indica la prioridad de la historia
        val_negocio: indica el valor de negocio de la historia
        val_tecnico: inidica el valor tecnico de la historia
        size: indica el tiempo estimado en horas en terminar la historia
        descripcion: una descripcion de la historia
        codigo: es el codigo de la historia
        acumulador: indica las horas trabajadas sobre la historia
        asignado: indica el usuario encargado de trabajar sobre la historia
        flujo: indica el flujo en que esta la historia
        estado: indica el estado en la actividad de un flujo en que esta la historia
        archivo: registra un archivo referente a la historia
        sprint: indica el sprint en que esta la historia
        asignado_p: indica si la historia esta asignada a un sprint o no
        activo: indica si la historia esta eliminada (False) o no (True)
        fecha: indica la fecha y la hora en que se crea una nueva version de la historia
    '''
    id_historia = models.ForeignKey(Historia)
    nombre = models.CharField(max_length=20)
    proyecto = models.ForeignKey(Proyecto, null=True)
    prioridad = models.IntegerField(default=0)
    val_negocio = models.IntegerField(default=0)
    val_tecnico = models.IntegerField(default=0)
    size = models.IntegerField(default=0)
    descripcion = models.CharField(max_length=100)
    codigo = models.CharField(max_length=5)
    acumulador = models.IntegerField(default=0)
    asignado = models.ForeignKey(Usuario, null=True)
    flujo = models.ForeignKey(Flujo, null=True)
    estado = models.CharField(max_length=5)
    actividad = models.CharField(max_length=20)
    #archivo = models.FilePathField
    sprint = models.CharField(max_length=20)
    asignado_p = models.BooleanField(default=False)
    activo = models.BooleanField(default=False)
    fecha = models.DateTimeField(null=True)

    def __unicode__(self):
        return self.nombre


class Registro(models.Model):
    '''
    Esta clase define el modelo de registro de tareas de una historia de usuario.
    Las informaciones a registrar son:
        id_historia: indica el id de la historia cuyas tareas se registran
        orden: indica el numero ordinal de la tarea realizada
        nombre: indica el nombre de la tarea realizada
        descripcion: breve descripcion de la tarea realizada
        horas: numero de horas trabajadas en realizar la tarea
    '''
    id_historia = models.ForeignKey(Historia)
    orden = models.IntegerField(default=0)
    nombre = models.CharField(max_length=20)
    proyecto = models.ForeignKey(Proyecto, null=True)
    descripcion = models.CharField(max_length=200)
    horas = models.IntegerField(default=0)
    fecha = models.DateTimeField(null=True)
    activo = models.BooleanField(default=False)

    def __unicode__(self):
        return self.nombre