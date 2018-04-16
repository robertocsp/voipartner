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
    valor_inicial_pretendido = models.FloatField(null=False, verbose_name='Pretenção para inestimento inicial', default=0)

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
    data_encerramento = models.DateField(blank=True, null=True)
    dia_aniversario = models.IntegerField(null=True, blank=True)
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
    percentual_lucro_mensal = models.FloatField(default=0.05)

    usuario = models.ForeignKey('Usuario', on_delete=models.PROTECT)

    status_choices = (
        ('1', 'pagamento pendente'),
        ('2', 'aguardando compensação'), #usuário fez upload do comprovante do pagamento.
        ('3', 'aguardando assinatura do contrato'), #após confirmação do pagamento elaboramos o contrato e enviamos ASSINADO para o cliente assinar via Docusign
        ('4', 'contrato em vigor'), #após assinatura do contrato, ele entra em vigor
        ('5', 'contrato encerrado'),  # após assinatura do contrato, ele entra em vigor

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

    def lista_lucro_por_mes(self):

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
            if dia_no_range.day is self.dia_aniversario and i != 0:
                lucro.dt_lucro = dia_no_range
                lucro.vl_lucro = lucro.vl_acumulado * self.percentual_lucro_mensal
                lucro.vl_lucro_acumulado = lucro.vl_lucro_acumulado + lucro.vl_lucro
                lucro.vl_acumulado = lucro.vl_acumulado + lucro.vl_lucro

                lucro_append = Lucro()
                lucro_append.dt_lucro = lucro.dt_lucro
                lucro_append.vl_lucro = lucro.vl_lucro
                lucro_append.vl_lucro_acumulado = lucro.vl_lucro_acumulado
                lucro_append.vl_acumulado = lucro.vl_acumulado

                lista_lucro.append(lucro_append)

        return lista_lucro

    def valor_acumulado(self):

        vl_acumulado = self.valor_contratado()

        hoje = datetime.date.today()
        delta = hoje - self.data_inicio_vigencia

        for i in range(delta.days):
            dia_no_range = datetime.date.fromordinal(self.data_inicio_vigencia.toordinal() + i)
            if dia_no_range.day is self.dia_aniversario and i != 0:
                lucro = vl_acumulado * self.percentual_lucro_mensal
                vl_acumulado = vl_acumulado + lucro

        return vl_acumulado

    def lucro_acumulado(self):

        vl_acumulado = self.valor_contratado()
        lucro_acumulado = 0

        hoje = datetime.date.today()
        delta = hoje - self.data_inicio_vigencia

        for i in range(delta.days):
            dia_no_range = datetime.date.fromordinal(self.data_inicio_vigencia.toordinal() + i)
            if dia_no_range.day is self.dia_aniversario and i != 0:
                lucro = vl_acumulado * self.percentual_lucro_mensal
                vl_acumulado = vl_acumulado + lucro
                lucro_acumulado = lucro_acumulado + lucro

        return lucro_acumulado

    def save(self, *args, **kwargs):
        #loga a mudança de status
        if self._state.adding is False:
            contrato = Contrato.objects.get(pk=self.pk)
            assunto = ""
            mensagem = ""
            destinatarios = []
            if contrato.status != self.status:
                self.log_mudanca_status = datetime.datetime.now()

                #envio de email funcionando, agora é aplicar as regras para notificacao

                if self.status is '2':
                    assunto = "Contrato aguardando compensação"
                    mensagem = "Prezado, você fez o upload do comprovante de depósito, estamos aguardando a compensação, assim que confirmada você será notificado. "
                    destinatarios = ['admin@voipartner.com', self.usuario.email]

                elif self.status is '3':
                    assunto = "Comprensação confirmada - Aguardando assinatura do contrato"
                    mensagem = "Prezado, o pagamento foi confirmado e seu contrato já está disponível para ser assinado eletronicamente. Clique aqui para acessar o nosso portal para acessar o seu contrato. Assim que confirmada a assinatura do seu contrato, você será notificado e seu contrato entrará em vigor"
                    destinatarios = [self.usuario.email]

                elif self.status is '4':
                    assunto = "Assinatura confirmada, seu contrato está em vigor"
                    mensagem = "Prezado, parabéns, seu contrato está ativo clique aqui e acompanhe a sua evolução."
                    destinatarios = [self.usuario.email]


                send_mail(
                    assunto,
                    mensagem,
                    'no-reply@voipartner.com',
                    destinatarios,
                    fail_silently=True,
                )



        else:
            assunto = "Seu contrato foi liberado"
            mensagem = "Prezado, seu contrato foi liberado e está com o status pendente de pagamento. Agora você deve realizar os seguintes passos: 1) entrar em www.voipartner.com/contratos, selecionar o contrato:  " + self.no_contrato + "e verificar quantas cotas foram liberadas para contratação; 2) realizar a transferencia para a conta da voi Partner: Dados bancarios; 3) Informar no site voipartner.com quantas cotas você adquiriu e fazer o upload do comprovante de transferencia e upload do seu documento de identificação; Assim que o valor for confirmado você receberá uma notificação por email"
            destinatarios = [self.usuario.email]

            send_mail(
                assunto,
                mensagem,
                'no-reply@voipartner.com',
                destinatarios,
                fail_silently=True,
            )




        super(Contrato, self).save()
