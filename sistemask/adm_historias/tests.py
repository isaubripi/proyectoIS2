from django.test import TestCase
from .models import Historia
from adm_proyectos.models import Proyecto
from adm_usuarios.models import Usuario

# Create your tests here.

class HistoriaTest(TestCase):

    '''
    Esta clase hace un prueba de creacion, modificacion y eliminacion de historias.
    Los campos de historia a probar son:
        nombre: nombre de la historia;
        descripcion: descripcion breve de la historia;
        proyecto: proyecto al que pertenece la historia;
        activo: determina si la historia esta activo o no en el proyecto.
    '''

    def setUp(self):
        print(':::::::::::Inicia pruebas unitarias de ABM HISTORIAS DE USUARIO:::::::::::')

        u1 = Usuario.objects.create(username= 'ruben',nombre = 'Ruben', apellido = 'Medina', password = 'ruben', cedula = 12345)


        historia1 = Historia.objects.create(nombre='Historia 1', descripcion='Historia Prueba 1', activo=True)
        historia2 = Historia.objects.create(nombre='Historia 2', descripcion='Historia Prueba 2', activo=True)

        print('Creacion de Historias ejecutada correctamente.')

    def test_modificar(self):


        historia1 = Historia.objects.update(nombre='Historia 1.1')
        historia2 = Historia.objects.update(nombre='Historia 2.1')
        print('Modificacion de Historia ejecutada correctamente.')

    def test_eliminar(self):

        historia1 = Historia.objects.get(nombre='Historia 1')
        historia2 = Historia.objects.get(nombre='Historia 1')

        historia1.delete()
        historia2.delete()
        print('Eliminacion de Historias ejecutada correctamente.')
