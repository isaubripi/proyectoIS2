from django.db import models
from adm_usuarios.models import Usuario
from adm_roles.models import Rol


class Cliente(models.Model):

    username= models.CharField(max_length=15, unique=True)
    nombre= models.CharField(max_length=50)
    apellido= models.CharField(max_length=50)
    password= models.CharField(max_length=10)
    cedula= models.CharField(max_length=10)
    email= models.CharField(max_length=20)
    estado= models.BooleanField(default=True)
    roles = models.ManyToManyField(Rol)

    def __unicode__(self):
        return self.nombre



class Proyecto(models.Model):
    """
    La clase proyecto contiene los siguientes atributos:
    - nombre: nombre que se le asignara al proyecto
    - descripcion: Un breve descripcion del proyecto
    - scrum_master: Usuario con la maxima autoridad dentro de un proyecto
    - scrum_team : Usuarios que pertenecen al proyecto
    - fecha_inicio : La fecha que dara inicio el proyecto
    - fecha_fin : La fecha de culminacion del proyecto
    - sprints : sprints asociados al proyecto
    - estado: Estado en el que se encuentra el proyecto.

    """
    estados_posibles= (
        ('I','iniciado'),
        ('N','noIniciado'),
        ('F','finalizado'),
    )

    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    scrum_master = models.ForeignKey(Usuario)
    scrum_team = models.ManyToManyField(Usuario,related_name= 'scrum_team' )
    fecha_inicio = models.DateField(null=True)
    fecha_fin = models.DateField(null=True)
    sprints = models.PositiveIntegerField(null=True)
    sprint_duracion = models.PositiveIntegerField(null= True)
    activo = models.BooleanField(default=True)
    estado= models.CharField ( max_length = 1 ,choices = estados_posibles,  default='N' )
    cliente = models.ForeignKey(Cliente, null=True)
    #flujos = models.ManyToManyField(Flujo)



def __unicode__(self):
    return self.nombre

