# Generated by Django 4.0.1 on 2022-02-18 04:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('unidadArea', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('correo', models.EmailField(max_length=255, unique=True, verbose_name='Correo Electrónico')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nombres')),
                ('last_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Apellidos')),
                ('avatar', models.ImageField(blank=True, max_length=255, null=True, upload_to='avatars/', verbose_name='Imagen de perfil')),
                ('estado', models.SmallIntegerField(default=1, null=True, verbose_name='Estado del usuario')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('unidadArea', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='unidadArea.unidadarea')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
            },
        ),
        migrations.CreateModel(
            name='HistoricalUser',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('correo', models.EmailField(db_index=True, max_length=255, verbose_name='Correo Electrónico')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Nombres')),
                ('last_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Apellidos')),
                ('avatar', models.TextField(blank=True, max_length=255, null=True, verbose_name='Imagen de perfil')),
                ('estado', models.SmallIntegerField(default=1, null=True, verbose_name='Estado del usuario')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('unidadArea', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='unidadArea.unidadarea')),
            ],
            options={
                'verbose_name': 'historical Usuario',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalContrasena_reinicio',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('correo', models.EmailField(db_index=True, max_length=255, verbose_name='Correo usuario')),
                ('token', models.CharField(db_index=True, max_length=40, verbose_name='token validador')),
                ('fechaCambio', models.DateTimeField(blank=True, editable=False, verbose_name='Fecha de Cambio')),
                ('estado', models.SmallIntegerField(default=1, null=True, verbose_name='Estado del token')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('usuario', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Contrasena_reinicio',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Contrasena_reinicio',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('correo', models.EmailField(max_length=255, unique=True, verbose_name='Correo usuario')),
                ('token', models.CharField(max_length=40, unique=True, verbose_name='token validador')),
                ('fechaCambio', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Cambio')),
                ('estado', models.SmallIntegerField(default=1, null=True, verbose_name='Estado del token')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Contrasena_reinicio',
                'verbose_name_plural': 'Contrasenas_reinicios',
            },
        ),
    ]
