from django.contrib import admin

from .models import *

# Register your models here.

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id','nome',)



@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = ('id','no_contrato','get_usuario','status','log_mudanca_status','data_criacao','data_inicio_vigencia','dia_aniversario', 'data_fim_adesao', 'data_renovacao_automatica', 'cotas_liberadas', 'valor_liberado', 'cotas_contratadas', 'valor_cota',)
    fields = ( 'no_contrato','usuario','status','data_inicio_vigencia','dia_aniversario', 'data_fim_adesao', 'data_renovacao_automatica', 'cotas_liberadas', 'cotas_contratadas', 'valor_cota', 'comprovante_deposito', 'link_contrato', 'contrato_assinado', 'observacao', 'percentual_lucro_mensal', 'data_encerramento',)

    def get_usuario(self,obj):
        return obj.usuario.nome
    get_usuario.short_description = 'Usuarios'
    get_usuario.admin_order_field = 'usuario__nome'


