
from django.db import models

class Usuario(models.Model):
    username= models.CharField(max_length=15, unique=True)
    nombre= models.CharField(max_length=50)
    apellido= models.CharField(max_length=50)
    password= models.CharField(max_length=10)
    cedula= models.CharField(max_length=10)
    email= models.CharField(max_length=20)
    estado= models.BooleanField(default=True)
    #permiso= models.ManyToManyField(Rol)

'''Un usuario posee los sgtes atributos:
username: Es el nombre que se utiliza para ingresar al sistema
nombre : Nombre del usuario
apellido : Apellido del usuario
Password : Contrasenha del usuario
cedula : nro de cedula del usuario
emial : direccion de correo electronico del usuario
estado : activo o inactivo, cuando esta inactivo sufio eliminacion logica'''

