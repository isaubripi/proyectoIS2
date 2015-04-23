from django.db import models
from adm_usuarios.models import Usuario
from adm_flujos.models import Flujo
from adm_proyectos.models import Proyecto

# Create your models here.

class Historia(models.Model):

    '''
    Esta clase define el modelo de historia de usuario.
    Los campos de este modelo son:
        nombre: nombre de la historia
        prioridad: indica la prioridad de la historia
        val_negocio: indica el valor de negocio de la historia
        val_tecnico: inidica el valor tecnico de la historia
        size: indica el tiempo estimado en horas en terminar la historia
        descripcion: una descripcion de la historia
        codigo: es el codigo de la historia
        acumulador: indica las horas trabajadas sobre la historia
        historial: registra un historial de la historia
        asignado: indica el usuario encargado de trabajar sobre la historia
        flujo: indica el flujo en que esta la historia
        estado: indica el estado en la actividad de un flujo en que esta la historia
        archivo: registra un archivo referente a la historia
        sprint: indica el sprint en que esta la historia
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
    historial = models.CharField(max_length=200)
    asignado = models.ForeignKey(Usuario, null=True)
    flujo = models.ForeignKey(Flujo, null=True)
    estado = models.CharField(max_length=5)
    #archivo = models.FilePathField
    #sprint = models.ForeignKey(Sprint, null=True)
    activo = models.BooleanField(default=False)


    def __unicode__(self):
        return self.nombre