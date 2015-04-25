from django.test import TestCase

# Create your tests here.

from adm_roles.models import Rol
from adm_usuarios.models import Usuario

class RolTest(TestCase):

    def setUp(self):
        print(':::::::::::Inicia pruebas unitarias de ABM ROL:::::::::::')
        rol1 = Rol.objects.create(nombre='primerrol')
        rol2 = Rol.objects.create(nombre='segundorol', activo=True, crear_proyecto=True)
        print('Creacion de roles ejectutada exitosamente')

    def test_nombre(self):
        rol1 = Rol.objects.get(nombre = 'primerrol')
        self.assertEqual(rol1.nombre, 'primerrol')
        print('Comparacion ejecutada exitosamente')

    def test_usuario(self):
        rol2 = Rol.objects.get(nombre= 'segundorol')
        self.assertEqual(rol2.nombre, 'segundorol')
        print('Comparacion ejecutada exitosamente')