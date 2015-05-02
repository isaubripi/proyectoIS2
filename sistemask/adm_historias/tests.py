from django.test import TestCase
from .models import Historia, Registro, Historial
from adm_proyectos.models import Proyecto
from adm_usuarios.models import Usuario
from django.utils import timezone

# Create your tests here.

class HistoriaTest(TestCase):

    '''
    Esta clase hace un prueba de creacion, modificacion y eliminacion de historias.
    Los campos de historia a probar son:
        nombre: nombre de la historia;
        descripcion: descripcion breve de la historia;
        proyecto: proyecto al que pertenece la historia;
        acumulador: horas trabajadas sobre la historia
        estado: estado actual de la historia
        activo: determina si la historia esta activo o no en el proyecto.
    '''

    def setUp(self):
        '''
        Prueba la creacion de historias.
        :return: nada
        '''
        print(':::::::::::Inicia pruebas unitarias de HISTORIAS DE USUARIO:::::::::::')

        u1 = Usuario.objects.create(username= 'ruben',nombre = 'Ruben', apellido = 'Medina', password = 'ruben', cedula = 12345)


        historia1 = Historia.objects.create(nombre='Historia 1', descripcion='Historia Prueba 1', activo=True)
        historia2 = Historia.objects.create(nombre='Historia 2', descripcion='Historia Prueba 2', activo=True)

        print('Creacion de Historias ejecutada correctamente.')

    def test_modificar(self):
        '''
        Prueba la modificacion de historia
        :return: nada
        '''

        historia1 = Historia.objects.update(nombre='Historia 1.1')
        historia2 = Historia.objects.update(nombre='Historia 2.1')
        print('Modificacion de Historia ejecutada correctamente.')

    def test_eliminar(self):
        '''
        Prueba la eliminacion de historia
        :return: nada
        '''

        historia1 = Historia.objects.get(nombre='Historia 1')
        historia2 = Historia.objects.get(nombre='Historia 1')

        historia1.delete()
        historia2.delete()
        print('Eliminacion de Historias ejecutada correctamente.')

    def test_cargarhoras(self):
        '''
        Prueba la carga de horas.
        :return: nada
        '''

        historia1 = Historia.objects.create(nombre='Historia1', descripcion='Historia1 prueba', activo=True)

        historia1.acumulador += 8
        print('Carga de horas efectuada correctamente')

    def test_cambiarestado(self):
        '''
        Prueba el cambio de estado.
        :return: nada
        '''

        historia2 = Historia.objects.create(nombre='Historia2', descripcion='Historia2 prueba', activo=True)
        historia2.estado = "To Do"
        historia2.estado = "Doing"
        historia2.estado = "Done"
        print('Cambio de estado realizado correctamente')

    def test_registrartareas(self):
        '''
        Prueba el registro de tareas de historia de usuario.
        :return:nada
        '''
        historia3 = Historia.objects.create(nombre='Historia3', descripcion='Historia3 prueba', activo=True)

        registro1 = Registro.objects.create(id_historia=historia3, nombre='tarea1', descripcion='Prueba de registro1')
        registro1.fecha = timezone.now()
        registro1.activo = True
        print('Registro de tareas correcto')