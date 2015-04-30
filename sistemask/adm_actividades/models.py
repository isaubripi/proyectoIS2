from django.db import models
from adm_proyectos.models import Proyecto

# Create your models here.

class Actividad(models.Model):
    """
    En esta clase se define el modelo de actividad
    Nombre: Nombre de la activdad
    Descripcion: Descripcion breve de la actividad
    Flujo: Flujo al cual pertenece la actividad
    Secuencia: Numero que indica en que posicion se encuentra la actividad dentro del flujo
    Estado : Si la actividad se encuentra activa o no activa
    Proyecto: Proyecto al cual pertenece la actividad

    """
    nombre = models.CharField(max_length=50)
    proyecto = models.ForeignKey(Proyecto, null=True)
    descripcion = models.CharField(max_length=200)
    flujo = models.PositiveIntegerField(max_length=10)
    secuencia = models.PositiveIntegerField(max_length=5)
    estado = models.BooleanField(default=False)
    asignado_h = models.BooleanField(default=False)

    def __unicode__(self):
        return self.nombre






