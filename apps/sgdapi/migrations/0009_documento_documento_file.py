# Generated by Django 4.0.1 on 2022-02-02 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sgdapi', '0008_alter_usuario_avatar_alter_usuario_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='documento',
            name='documento_file',
            field=models.FileField(blank=True, null=True, upload_to='files/', verbose_name='Archivo del documento'),
        ),
    ]
