# Generated by Django 4.0.1 on 2022-01-29 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sgdapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contrasena_reinicio',
            name='estado',
            field=models.SmallIntegerField(default=1, null=True, verbose_name='Estado del token'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='avatar',
            field=models.CharField(blank=True, default='/default.jpg', max_length=255, null=True, verbose_name='Imagen del usuario'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='correo',
            field=models.CharField(max_length=255, unique=True, verbose_name='Correo electronico'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='estado',
            field=models.SmallIntegerField(default=0, null=True, verbose_name='Estado del usuario'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='fecha_actualizacion',
            field=models.DateField(auto_now_add=True, verbose_name='Fecha de actualizacion'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='fecha_creacion',
            field=models.DateField(auto_now=True, verbose_name='Fecha de Creacion'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='nombreUsuario',
            field=models.CharField(max_length=255, unique=True, verbose_name='Nombres del Usuario'),
        ),
    ]
