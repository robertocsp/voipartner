from django.forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class UsuarioForm(ModelForm):
    password1 = CharField(widget=PasswordInput())
    password2 = CharField(widget=PasswordInput())
    email_confirmacao = EmailField()

    class Meta:
        model = Usuario
        fields = [
            'nome',
            'email',
            'email_confirmacao',
            'telefone',
            'documento_identificacao',
            'data_nascimento',
            'endereco',
            'cidade',
            'estado',
            'cep',
            'valor_inicial_pretendido',
            'password1',
            'password2',
        ]

    def save(self, username, raw_password, *args, **kwargs):
        instance = super(UsuarioForm, self).save(commit=False)
        instance.save(username, raw_password)
        return instance


class LoginForm(Form):
    username = CharField(max_length=100, label='email')
    password = CharField(widget=PasswordInput(), label='senha')


class ContratoPendentePagamentoForm(ModelForm):
    cotas_contratadas = IntegerField()
    comprovante_deposito = FileField()


    class Meta:
        model = Contrato
        fields = [
            'cotas_contratadas',
            'comprovante_deposito',

        ]

    def save(self, *args, **kwargs):
        instance = super(ContratoPendentePagamentoForm, self).save(commit=False)
        instance.status = '2'
        instance.save()
        return instance



