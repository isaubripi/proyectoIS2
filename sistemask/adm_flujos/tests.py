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

    def setUp(self):
        print(':::::::::::Inicia pruebas unitarias de ABM FLUJO:::::::::::')

        flujo1 = Flujo.objects.create(nombre='Flujo Desarrollo 1', descripcion='Flujo Prueba 1', activo=True)
        flujo2 = Flujo.objects.create(nombre='Flujo Desarrollo 2', descripcion='Flujo Prueba 2', activo=True)

        print('Creacion de Flujos ejecutada correctamente.')

    def test_modificar(self):

        flujo1 = Flujo.objects.update(nombre='Flujo Desarrollo 1.1')
        flujo2 = Flujo.objects.update(nombre='Flujo Desarrollo 2.1')
        print('Modificacion de Flujos ejecutada correctamente.')

    def test_eliminar(self):
        flujo1 = Flujo.objects.get(nombre='Flujo Desarrollo 1')
        flujo1.delete()
        print('Eliminacion de Flujos ejecutada correctamente.')
