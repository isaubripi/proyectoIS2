from django.db import models
from adm_proyectos.models import Proyecto

#prueba

# Create your models here.

class Flujo(models.Model):

    nombre = models.CharField(max_length=50)
    proyecto = models.ForeignKey(Proyecto, null=True)
    descripcion = models.CharField(max_length=100)
    activo = models.BooleanField(default=False)
    #actividades = models.ManyToManyField(Actividad)

    def __unicode__(self):
        return self.nombre




