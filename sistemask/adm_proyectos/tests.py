from django.test import TestCase

from adm_usuarios.models import Usuario
from adm_proyectos.models import Proyecto

# Create your tests here.
class ProyectoTest(TestCase):
    """
    En es la clase encargara de realizar las pruebas unitarias
    basicamente se prueban la creacion, modificacion y eliminacion
    """


    def setUp(self):
        print(':::::::::::Inicia pruebas unitarias de ABM PROYECTO:::::::::::')

        u1 = Usuario.objects.create(username= 'isidro',nombre = 'Isidro', apellido = 'Brizuela', password = 'isidro', cedula = 3841270)

        Proyecto.objects.create(nombre= 'Sistema de informacion 1', descripcion= 'Escrito en java',scrum_master=u1, fecha_inicio='2015-05-15', fecha_fin='2015-05-17', activo=True )
        Proyecto.objects.create(nombre= 'Sistema de informacion 2', descripcion= 'Escrito en python',scrum_master=u1, fecha_inicio='2015-05-15', fecha_fin='2015-05-17', activo=True )
        Proyecto.objects.create(nombre= 'Sistema de informacion 3', descripcion= 'Escrito en c++',scrum_master=u1, fecha_inicio='2015-05-15', fecha_fin='2015-05-17', activo=True )

        print('Creacion de Proyectos ejecutada correctamente.')

    def test_modificacion(self):
        """
        Se modifica el nombre de cada uno de los proyectos creados
        :return:Nada
        """
        P1 = Proyecto.objects.get(nombre='Sistema de informacion 1')
        P1.nombre = 'SISTEMA DE INFORMACION 1'
        P1.save()

        print('Modificacion de Proyectos ejecutada exitosamente')


    def test_eliminacion(self):
        """
        Se eliminan los 3 proyectos creados.
        :return:Nada
        """
        P2 = Proyecto.objects.get(nombre= 'Sistema de informacion 2')
        P2.delete()

        print('Eliminacion de Proyectos ejecutada exitosamente')

    def test_inicializar(self):

        u2 = Usuario.objects.create(username= 'juan',nombre = 'Isidro', apellido = 'Brizuela', password = 'isidro', cedula = 3841270)
        P3 = Proyecto.objects.get(nombre= 'Sistema de informacion 3')

        P3.scrum_team.add(u2)

        print('Proyecto Inicializado exitosamente')