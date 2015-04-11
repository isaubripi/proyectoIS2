from django.test import TestCase

# Create your tests here.

from adm_roles.models import Rol
from adm_usuarios.models import Usuario

class RolTest(TestCase):
    def setUp(self):
        rol1 = Rol.objects.create(nombre='primerrol')
        rol2 = Rol.objects.create(nombre='segundorol', activo=True, crear_proyecto=True)

    def test_nombre(self):
        rol1 = Rol.objects.get(nombre = 'primerrol')
        self.assertEqual(rol1.nombre, 'primerrol')

    #def test_usuario(self):
        #rol2 = Usuario.objects.get(usuario= 'juan')
        #self.assertEqual(rol2.nombre, 'juan')