from django.test import TestCase

from adm_usuarios.models import Usuario
from adm_sprints.models import Sprint
from .models import Proyecto
from adm_sprints.models import Equipo

# Create your tests here.
class SprintTest(TestCase):
    """
    En es la clase encargara de realizar las pruebas unitarias
    basicamente se prueban la creacion, modificacion y eliminacion
    """


    def setUp(self):
        """
        Se crean 3 objetos tipo Proyecto y se asigan a cada sprint
        :return:Nada
        """
        print(':::::::::::Inicia pruebas unitarias de ABM SPRINT:::::::::::')

        u1 = Usuario.objects.create(username= 'isidro',nombre = 'Isidro', apellido = 'Brizuela', password = 'isidro', cedula = 3841270)


        Proyecto1 = Proyecto.objects.create(nombre= 'Sistema de informacion 1', descripcion= 'Escrito en java', scrum_master=u1, fecha_inicio='2015-05-15', fecha_fin='2015-05-17', activo=True )
        Proyecto2 = Proyecto.objects.create(nombre= 'Sistema de informacion 2', descripcion= 'Escrito en python', scrum_master=u1, fecha_inicio='2015-05-15', fecha_fin='2015-05-17', activo=True )
        Proyecto3 = Proyecto.objects.create(nombre= 'Sistema de informacion 3', descripcion= 'Escrito en c++', scrum_master=u1, fecha_inicio='2015-05-15', fecha_fin='2015-05-17', activo=True )

        Sprint.objects.create(nombre='Sprint 1', descripcion= 'Nada', fecha_inicio= '2015-05-15', fecha_fin='2015-06-15', duracion=30, proyecto=Proyecto1)
        Sprint.objects.create(nombre='Sprint 2', descripcion= 'Nada', fecha_inicio= '2015-05-15', fecha_fin='2015-06-15', duracion=30, proyecto=Proyecto2)
        Sprint.objects.create(nombre='Sprint 3', descripcion= 'Nada', fecha_inicio= '2015-05-15', fecha_fin='2015-06-15', duracion=30, proyecto=Proyecto3)

        print('Creacion de Sprints ejecutada correctamente.')

    def test_modificacion(self):
        """
        Se modifica el nombre de un sprint creado previamente
        :return:Nada
        """
        S1= Sprint.objects.get(nombre='Sprint 1')
        S1.nombre = 'Sprint1'
        S1.save()

        print('Modificacion de Sprints ejecutada correctamente.')

    def test_eliminacion(self):
        """
        Se elimina un sprint creado previamente
        :return:Nada
        """
        S2 = Sprint.objects.get(nombre= 'Sprint 2')
        S2.delete()

        print('Eliminacion de Sprints ejecutada correctamente.')

    def test_activacion(self):
        """
        Se activa un sprint creado previamente
        :return:nada
        """
        S3 = Sprint.objects.get(nombre='Sprint 3')
        S3.estado = 'A'
        S3.save()

        print('Activacion de Sprints ejecutada correctamente.')

    def test_equipo(self):
        """
        Se asigna equipo a un sprint
        :return:nada
        """
        u1 = Usuario.objects.create(username= 'juan',nombre = 'Isidro', apellido = 'Brizuela', password = 'isidro', cedula = 3841270)
        S3 = Sprint.objects.get(nombre='Sprint 3')
        E = Equipo()
        E.usuario = u1
        E.horas_sprint = 5
        E.save()
        S3.equipo.add(E)
        S3.save()

        print('Asignacion de equipo a Sprint ejecutada correctamente.')

    def test_estado(self):
        """
        Se cambia el estado a un sprint
        :return:nada
        """

        S3 = Sprint.objects.get(nombre='Sprint 3')
        S3.estado = 'En Ejecucio'
        S3.save()

        print('Cambio de estado a Sprint ejecutado correctamente.')
