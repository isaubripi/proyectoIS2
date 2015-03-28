from django.test import TestCase

from adm_usuarios.models import Usuario

# Create your tests here.

class UserTest(TestCase):
    def setUp(self):
        u1 = Usuario.objects.create(username= 'isidro',nombre = 'Isidro', apellido = 'Brizuela', password = 'isidro', cedula = 3841270, email='isaubripi@gmail.com', estado = True)
        u2 = Usuario.objects.create(username= 'juan',nombre = 'Juan', apellido = 'Benitez', password = 'juan', cedula = 3841270, email='isaubripi@gmail.com', estado = True)

    def test_user(self):
        u1 = Usuario.objects.get(username = 'isidro')
        self.assertEqual(u1.username, 'isidro')

    def test_name(self):
        u1 = Usuario.objects.get(nombre= 'Isidro')
        self.assertEqual(u1.nombre, 'Isidro')


