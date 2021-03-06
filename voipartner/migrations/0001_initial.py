# Generated by Django 2.0.3 on 2018-03-26 18:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contrato',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_contrato', models.CharField(max_length=10)),
                ('data_criacao', models.DateField(auto_now=True)),
                ('data_inicio_vigencia', models.DateField(blank=True, null=True)),
                ('data_fim_adesao', models.DateField(blank=True, null=True)),
                ('data_renovacao_automatica', models.DateField(blank=True, null=True)),
                ('dia_aniversario', models.IntegerField(blank=True, null=True)),
                ('taxa_lucro_prefixado', models.IntegerField(null=True)),
                ('cotas_liberadas', models.IntegerField(null=True)),
                ('cotas_contratadas', models.IntegerField(null=True)),
                ('valor_cota', models.FloatField(null=True)),
                ('status', models.CharField(choices=[('1', 'pagamento pendente'), ('2', 'contrato em vigor')], max_length=2, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Status_Contrato',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=40, null=True)),
                ('descricao', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('telefone', models.CharField(max_length=30, null=True)),
                ('documento_identificacao', models.CharField(max_length=60, null=True)),
                ('data_nascimento', models.DateField(blank=True, null=True)),
                ('endereco', models.CharField(max_length=200, null=True)),
                ('cidade', models.CharField(max_length=60, null=True)),
                ('estado', models.CharField(max_length=2, null=True)),
                ('cep', models.CharField(max_length=10, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='contrato',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='voipartner.Usuario'),
        ),
    ]
