from django.db import models
from django.contrib.auth.models import User
import datetime
from django.core.mail import send_mail


# Create your models here.

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=100, null=False)
    email = models.EmailField(max_length=100, null=False)
    telefone = models.CharField(max_length=30, null=True)
    documento_identificacao = models.CharField(max_length=60, null=True)
    data_nascimento = models.DateField(null=True, blank=True)
    endereco = models.CharField(max_length=200, null=True)
    cidade = models.CharField(max_length=60, null=True)
    estado = models.CharField(max_length=2, null=True)
    cep = models.CharField(max_length=10, null=True)
    upload_documento_identificacao = models.FileField(null=True, blank=True)
    valor_inicial_pretendido = models.FloatField(null=False, verbose_name='Valor de investimento inicial', default=0)

    def __str__(self):
        return self.nome

    def get_nome_by_user(user):
        usuario = Usuario.objects.get(user=user)
        return usuario.nome

    def get_usuario_by_user(user):
        usuario = Usuario.objects.get(user=user)
        return usuario

class Contrato(models.Model):
    no_contrato = models.CharField(max_length=10)
    data_criacao = models.DateField(auto_now=True)
    data_inicio_vigencia = models.DateField(blank=True, null=True)
    data_fim_adesao = models.DateField(blank=True, null=True)  # 90 dias apos o inicio da vigencia
    data_renovacao_automatica = models.DateField(blank=True, null=True)  # 6 meses após o início da vigência
    dia_aniversario = models.IntegerField(null=True, blank=True)
    taxa_lucro_prefixado = models.IntegerField(null=True)
    comprovante_deposito = models.FileField(null=True, blank=True)
    link_contrato = models.TextField(null=True, blank=True)
    contrato_assinado = models.FileField(null=True, blank=True)
    log_mudanca_status = models.DateTimeField(blank=True, null=True)
    # bonus --> cada contrato poderá ter bonus de acordo com a evolução dos negócios.
    detalhamento_resgate = models.FileField(null=True, blank=True)
    cotas_liberadas = models.IntegerField(null=True)
    cotas_contratadas = models.IntegerField(null=True)
    valor_cota = models.FloatField(null=True)
    observacao = models.TextField(null=True, blank=True)

    usuario = models.ForeignKey('Usuario', on_delete=models.PROTECT)

    status_choices = (
        ('1', 'pagamento pendente'),
        ('2', 'aguardando compensação'), #usuário fez upload do comprovante do pagamento.
        ('3', 'aguardando assinatura do contrato'), #após confirmação do pagamento elaboramos o contrato e enviamos ASSINADO para o cliente assinar via Docusign
        ('4', 'contrato em vigor'), #após assinatura do contrato, ele entra em vigor

    )
    status = models.CharField(
        max_length=2,
        choices=status_choices,
        null=True,
    )

    def valor_liberado(self):
        return self.cotas_liberadas * self.valor_cota

    def valor_contratado(self):
        # if self.cotas_contratadas is not None & self.valor_cota is not None:
        return self.cotas_contratadas * self.valor_cota

    def lucro_acumulado(self):

        class Lucro:
            dt_lucro = None
            vl_lucro = None
            vl_lucro_acumulado = None
            vl_acumulado = None

        hoje = datetime.date.today()
        delta = hoje - self.data_inicio_vigencia

        lucro = Lucro()
        lucro.vl_lucro = 0
        lucro.vl_lucro_acumulado = 0
        lucro.vl_acumulado = self.valor_contratado()
        lista_lucro = []

        for i in range(delta.days):
            dia_no_range = datetime.date.fromordinal(self.data_inicio_vigencia.toordinal() + i)
            if dia_no_range.day == self.dia_aniversario & i != 0:
                lucro.dt_lucro = dia_no_range
                lucro.vl_lucro = lucro.vl_acumulado * 0.05
                lucro.vl_lucro_acumulado = lucro.vl_lucro_acumulado + lucro.vl_lucro
                lucro.vl_acumulado = lucro.vl_acumulado + lucro.vl_lucro

                lucro_append = Lucro()
                lucro_append.dt_lucro = lucro.dt_lucro
                lucro_append.vl_lucro = lucro.vl_lucro
                lucro_append.vl_lucro_acumulado = lucro.vl_lucro_acumulado
                lucro_append.vl_acumulado = lucro.vl_acumulado

                lista_lucro.append(lucro_append)

        return lista_lucro

    def save(self, *args, **kwargs):
        #loga a mudança de status
        if self._state.adding is False:
            contrato = Contrato.objects.get(pk=self.pk)
            if contrato.status != self.status:
                self.log_mudanca_status = datetime.datetime.now()

                #envio de email funcionando, agora é aplicar as regras para notificacao


                mensagem = "Prezado, o status do seu contrato foi alterado, entre no site e veja "

                '''
                send_mail(
                    'assunto teste envio email via django',
                    'Mensagem teste',
                    'no-reply@voipartner.com',
                    ['80.pereira@gmail.com'],
                    fail_silently=True,
                )
                '''
        else:
            mensagem = "Prezado, seu contrato foi liberado para "



        super(Contrato, self).save()
