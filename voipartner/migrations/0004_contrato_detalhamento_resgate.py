# Generated by Django 2.0.3 on 2018-04-07 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voipartner', '0003_auto_20180407_0045'),
    ]

    operations = [
        migrations.AddField(
            model_name='contrato',
            name='detalhamento_resgate',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]