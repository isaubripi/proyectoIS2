from django.test import TestCase

from adm_usuarios.models import Usuario
from .models import Proyecto

# Create your tests here.
class ProyectoTest(TestCase):
    """
    En es la clase encargara de realizar las pruebas unitarias
    basicamente se prueban la creacion, modificacion y eliminacion
    """
    print('Inicia pruebas unitarias de ABM PROYECTO')

    def creacion(self):
        u1 = Usuario.objects.create(username= 'isidro',nombre = 'Isidro', apellido = 'Brizuela', password = 'isidro', cedula = 3841270, email='isaubripi@gmail.com', estado = True)

        Proyecto1 = Proyecto.objects.create(nombre= 'Sistema de informacion 1', descripcion= 'Escrito en java', scrum_master=u1, scrum_team=u1,  fecha_inicio='2015-05-15', fecha_fin='2015-05-17', activo=True )
        #Proyecto2 = Proyecto.objects.create(nombre= 'Sistema de informacion 2', descripcion= 'Escrito en python', scrum_master= Usuario.objects.create(nombre='Juan'), scrum_team= Usuario.objects.create(nombre='Juan'), fecha_inicio='2015-05-15', fecha_fin='2015-05-17', activo=True )
        #Proyecto3 = Proyecto.objects.create(nombre= 'Sistema de informacion 3', descripcion= 'Escrito en c++', scrum_master= Usuario.objects.create(nombre='Ruben'), scrum_team= Usuario.objects.create(nombre='Ruben'), fecha_inicio='2015-05-15', fecha_fin='2015-05-17', activo=True )

        print('Creacion de Proyectos ejecutada correctamente.')

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
