# Generated by Django 4.0.1 on 2022-01-29 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sgdapi', '0004_alter_usuario_correo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contrasena_reinicio',
            name='correo',
            field=models.EmailField(max_length=255, verbose_name='Correo usuario'),
        ),
    ]