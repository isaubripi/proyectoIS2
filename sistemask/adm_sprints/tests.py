from django.test import TestCase

from adm_usuarios.models import Usuario
from adm_sprints.models import Sprint
from .models import Proyecto

# Create your tests here.
class ProyectoTest(TestCase):
    """
    En es la clase encargara de realizar las pruebas unitarias
    basicamente se prueban la creacion, modificacion y eliminacion
    """
    print('Inicia pruebas unitarias de ABM SPRINT')

    def creacion(self):
        """
        Se crean 3 objetos tipo Proyecto
        :return:Nada
        """
        Proyecto1 = Proyecto.objects.create(nombre= 'Sistema de informacion 1', descripcion= 'Escrito en java', scrum_master= Usuario.objects.create(nombre='Isidro'), scrum_team= Usuario.objects.create(nombre='Isidro'), fecha_inicio='2015-05-15', fecha_fin='2015-05-17', activo=True )
        Proyecto2 = Proyecto.objects.create(nombre= 'Sistema de informacion 2', descripcion= 'Escrito en python', scrum_master= Usuario.objects.create(nombre='Juan'), scrum_team= Usuario.objects.create(nombre='Juan'), fecha_inicio='2015-05-15', fecha_fin='2015-05-17', activo=True )
        Proyecto3 = Proyecto.objects.create(nombre= 'Sistema de informacion 3', descripcion= 'Escrito en c++', scrum_master= Usuario.objects.create(nombre='Ruben'), scrum_team= Usuario.objects.create(nombre='Ruben'), fecha_inicio='2015-05-15', fecha_fin='2015-05-17', activo=True )

        Sprint1 = Sprint.objects.create(nombre='Sprint 1', descripcion= 'Nada', fecha_inicio= '2015-05-15', fecha_fin='2015-06-15', duracion=30, proyecto=Proyecto1)
        Sprint2 = Sprint.objects.create(nombre='Sprint 2', descripcion= 'Nada', fecha_inicio= '2015-05-15', fecha_fin='2015-06-15', duracion=30, proyecto=Proyecto2)
        Sprint3 = Sprint.objects.create(nombre='Sprint 3', descripcion= 'Nada', fecha_inicio= '2015-05-15', fecha_fin='2015-06-15', duracion=30, proyecto=Proyecto3)

        print('Creacion de Sprints ejecutada correctamente.')

    '''def modificacion(self):
        """
        Se modifica el nombre de cada uno de los proyectos creados
        :return:Nada
        """
        Proyecto1 = Proyecto.objects.update(nombre='Sistema de informacion 3')
        Proyecto2 = Proyecto.objects.update(nombre='Sistema de informacion 2')
        Proyecto3 = Proyecto.objects.update(nombre='Sistema de informacion 1')


    def eliminacion(self):
        """
        Se eliminan los 3 proyectos creados.
        :return:Nada
        """
        Proyecto1 = Proyecto.objects.delete()
        Proyecto2 = Proyecto.objects.delete()
        Proyecto3 = Proyecto.objects.delete()'''
