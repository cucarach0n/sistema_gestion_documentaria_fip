# Generated by Django 4.0.1 on 2022-02-05 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_rename_image_historicaluser_avatar_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaluser',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
