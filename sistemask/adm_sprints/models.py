from django.db import models

# Create your models here.
from adm_proyectos.models import Proyecto

class Sprint(models.Model):
    """
    nombre : Nombre que se le asignara al sprint
    descripcion : Informacion adicional para el sprint
    fecha_inicio: fecha en donde comenzara el sprint
    fecha_fin: fecha en donde terminara el sprint
    duracion: cantidad en dias del sprint
    proyecto: proyecto al cual pertenece el sprint
    activo: estado del sprint
    estado: Estado interno del sprint P o A
    """

    estados_posibles= (
        ('P','Planificado'),
        ('A','Activado'),)

    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    fecha_inicio = models.DateField(null=True)
    fecha_fin = models.DateField(null=True)
    duracion = models.PositiveIntegerField(null=True)
    proyecto = models.ForeignKey(Proyecto)
    activo = models.BooleanField(default=True)
    estado = models.CharField(max_length=1, choices= estados_posibles, default='P')

def __unicode__(self):
    return self.nombre

