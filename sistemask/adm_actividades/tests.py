from django.test import TestCase

from adm_usuarios.models import Usuario
from adm_sprints.models import Sprint
from adm_actividades.models import Actividad
from adm_proyectos.models import Proyecto

# Create your tests here.
class SprintTest(TestCase):
    """
    En es la clase encargara de realizar las pruebas unitarias
    basicamente se prueban la creacion, modificacion y eliminacion
    """


    def setUp(self):
        """
        Se crean 3 objetos tipo Proyecto y se asigan a cada actividad
        :return:Nada
        """
        print(':::::::::::Inicia pruebas unitarias de ABM ACTIVIDAD:::::::::::')

        u1 = Usuario.objects.create(username= 'isidro',nombre = 'Isidro', apellido = 'Brizuela', password = 'isidro', cedula = 3841270)


        Proyecto1 = Proyecto.objects.create(nombre= 'Sistema de informacion 1', descripcion= 'Escrito en java', scrum_master=u1, fecha_inicio='2015-05-15', fecha_fin='2015-05-17', activo=True )
        Proyecto2 = Proyecto.objects.create(nombre= 'Sistema de informacion 2', descripcion= 'Escrito en python', scrum_master=u1, fecha_inicio='2015-05-15', fecha_fin='2015-05-17', activo=True )
        Proyecto3 = Proyecto.objects.create(nombre= 'Sistema de informacion 3', descripcion= 'Escrito en c++', scrum_master=u1, fecha_inicio='2015-05-15', fecha_fin='2015-05-17', activo=True )

        Actividad.objects.create(nombre='Analisis', descripcion= 'Nada', proyecto=Proyecto1,flujo=1, secuencia=0 )
        Actividad.objects.create(nombre='Diagramacion', descripcion= 'Nada', proyecto=Proyecto2, flujo=1, secuencia =0)
        Actividad.objects.create(nombre='Implementacion', descripcion= 'Nada', proyecto=Proyecto3, flujo=1, secuencia=0)

        print('Creacion de Actividades ejecutada correctamente.')

    def test_modificacion(self):
        """
        Se modifica el nombre de una actividad creada previamente
        :return:Nada
        """
        A1= Actividad.objects.get(nombre='Analisis')
        A1.nombre = 'ANALISIS'
        A1.save()

        print('Modificacion de Actividades ejecutada correctamente.')

    def test_eliminacion(self):
        """
        Se elimina una actividad creada previamente
        :return:Nada
        """
        A2 = Actividad.objects.get(nombre= 'Diagramacion')
        A2.delete()

        print('Eliminacion de Actividades ejecutada correctamente.')

    def test_secuencia(self):
        """
        Se establece la secuencia de una actividad creada previamente
        :return:nada
        """
        A3 = Actividad.objects.get(nombre='Implementacion')
        A3.secuencia = 3
        A3.save()

        print('Establecimiento de secuencia de Actividades ejecutada correctamente.')

    def test_secuencia2(self):
        """
        Se restablece la secuencia de una actividad creada previamente
        :return:nada
        """
        A3 = Actividad.objects.get(nombre='Implementacion')
        A3.secuencia = 1
        A3.save()

        print('Restablecimiento de secuencia de Actividades ejecutada correctamente.')

    def test_cambiarproyecto(self):
        """
        Se cambia el proyecto de una actividad creada previamente
        :return:nada
        """
        u1 = Usuario.objects.create(username= 'juan',nombre = 'Isidro', apellido = 'Brizuela', password = 'isidro', cedula = 3841270)
        Proyecto1 = Proyecto.objects.create(nombre= 'Sistema de informacion 1', descripcion= 'Escrito en java', scrum_master=u1, fecha_inicio='2015-05-15', fecha_fin='2015-05-17', activo=True )
        A3 = Actividad.objects.get(nombre='Implementacion')
        A3.proyecto= Proyecto1
        A3.save()

        print('Cambio de proyecto de Actividades ejecutada correctamente.')

    def test_cambiardescripcion(self):
        """
        Se cambia la descripcion de una actividad creada previamente
        :return:nada
        """

        A3 = Actividad.objects.get(nombre='Implementacion')
        A3.descripcion = 'Cambio de descripcion'
        A3.save()

        print('Cambio de descripcion de Actividades ejecutada correctamente.')