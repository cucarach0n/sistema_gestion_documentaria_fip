# Generated by Django 4.0.1 on 2022-02-05 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sgdapi', '0013_alter_documento_extension_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documento',
            name='documento_file',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='Archivo del documento'),
        ),
    ]
