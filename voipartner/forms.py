from django.forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class UsuarioForm(ModelForm):
    password1 = CharField(widget=PasswordInput())
    password2 = CharField(widget=PasswordInput())

    def save(self, username, raw_password, *args, **kwargs):
        instance = super(UsuarioForm, self).save(commit=False)
        instance.save(username,raw_password)
        return instance

    class Meta:
        model = Usuario
        fields = [
            'nome',
            'email',
            'telefone',
            'documento_identificacao',
            'data_nascimento',
            'endereco',
            'cidade',
            'estado',
            'cep',
            'password1',
            'password2',
        ]


class LoginForm(Form):
    username = CharField(max_length=100, label='email')
    password = CharField(widget=PasswordInput(), label='senha')


