from django.forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django.core.exceptions import ValidationError


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

    ''' Ajustar a validação por campo
    def clean_email(self):
        field = self.cleaned_data['email']
        insert = self.instance.pk == None
        usuario_existente = Usuario.objects.get(email=field) == None

        if insert and usuario_existente:
            raise forms.ValidationError('Usuario existente - email: ' + field)
        else:
            pass
        return field
    '''

    def save(self, username, raw_password, *args, **kwargs):
        instance = super(UsuarioForm, self).save(commit=False)

        if self.instance.pk == None:
            user = User.objects.create_user(username=username, password=raw_password)
            instance.user = user


        instance.save()
        return instance

    '''
    def is_valid(self):
        instance = super(UsuarioForm, self).save(commit=False)
        if instance.data_nascimento > datetime.datetime.now().date():
            raise ValidationError(('Data de nascimento maior que hoje, usuário não nasceu'), code='nao_nasceu')
        return True
    '''

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



