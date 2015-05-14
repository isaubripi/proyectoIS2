from django.db import models

# Create your models here.
from adm_proyectos.models import Proyecto
from adm_historias.models import Historia
from adm_usuarios.models import Usuario

class Equipo(models.Model):
    """
    usuario: aquel usuario que es parte de un sprint
    horas_sprint: cantidad de horas por dia que un usuario trabajara dentro del sprint
    """
    usuario=models.ForeignKey(Usuario)
    horas_sprint=models.PositiveIntegerField(null=True)



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
    historias: Aquellas historias de usuario que son asignadas al sprint
    """

    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    fecha_inicio = models.DateField(null=True)
    fecha_fin = models.DateField(null=True)
    duracion = models.PositiveIntegerField(null=True)
    proyecto = models.ForeignKey(Proyecto)
    activo = models.BooleanField(default=True)
    estado = models.CharField(max_length=15, default='Futuro')
    historias = models.ManyToManyField(Historia, related_name='historias')
    asignado_h = models.BooleanField(default=False)
    equipo = models.ManyToManyField(Equipo, default=False)

def __unicode__(self):
    return self.nombre




