# Generated by Django 2.0.3 on 2018-04-09 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voipartner', '0005_usuario_upload_documento_identificacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='contrato',
            name='observacao',
            field=models.TextField(blank=True, null=True),
        ),
    ]
