# Generated by Django 4.0.1 on 2022-02-13 23:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sgdapi', '0019_alter_folderinfolder_child_folder_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fileinfolder',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='folderinfolder',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='historicalfileinfolder',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='historicalfolderinfolder',
            name='slug',
        ),
    ]
