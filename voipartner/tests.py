from django.test import TestCase
from .models import *

# Create your tests here.


class UsuarioModelTests(TestCase):
    def test_usuario_nao_nascido(self):
        '''
        Espera que a data de nascimento seja maior que o dia de hoje
        :return:
        '''
        data_futura = datetime.datetime.now().date() + datetime.timedelta(days=1)
        usuario = Usuario(nome='teste criacao usuario', email='testecriausu@teste.com', data_nascimento=data_futura)
        usuario.save('testeautomatizado', '123')
        self.assertLess(usuario.data_nascimento, datetime.datetime.now())
