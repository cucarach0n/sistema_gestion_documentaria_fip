# Generated by Django 4.0.1 on 2022-02-06 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_historicaluser_is_active_alter_user_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaluser',
            name='nombreUsuario',
            field=models.CharField(db_index=True, max_length=255, verbose_name='Correo Electrónico'),
        ),
        migrations.AlterField(
            model_name='user',
            name='nombreUsuario',
            field=models.CharField(max_length=255, unique=True, verbose_name='Correo Electrónico'),
        ),
    ]