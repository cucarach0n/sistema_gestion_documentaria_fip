# Generated by Django 4.0.1 on 2022-02-04 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sgdapi', '0012_alter_documento_nombredocumento_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documento',
            name='extension',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Extension de los archivos subidos'),
        ),
        migrations.AlterField(
            model_name='historicaldocumento',
            name='extension',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Extension de los archivos subidos'),
        ),
    ]