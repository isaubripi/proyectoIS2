from django.test import TestCase
from models import Flujo
from adm_proyectos.models import Proyecto

# Create your tests here.

class FlujoTest(TestCase):

    '''
    Esta clase hace un prueba de creacion, modificacion y eliminacion de flujos.
    Los campos del flujo son:
        nombre: nombre del flujo;
        descripcion: descripcion breve del flujo;
        proyecto: proyecto al que pertenece el flujo;
        activo: determina si el flujo esta activo o no en el proyecto.
    '''

    def crear(self):

        flujo1 = Flujo.objects.create(nombre='Flujo Desarrollo 1', descripcion='Flujo Prueba 1', proyecto=Proyecto.objects.create(nombre='Proyecto 1'), activo=True)
        flujo2 = Flujo.objects.create(nombre='Flujo Desarrollo 2', descripcion='Flujo Prueba 2', proyecto=Proyecto.objects.create(nombre='Proyecto 2'), activo=True)

    def modificar(self):

        flujo1 = Flujo.objects.update(nombre='Flujo Desarrollo 1.1')
        flujo2 = Flujo.objects.update(nombre='Flujo Desarrollo 2.1')

    def eliminar(self):

        flujo1 = Flujo.objects.delete()
        flujo2 = Flujo.objects.delete()