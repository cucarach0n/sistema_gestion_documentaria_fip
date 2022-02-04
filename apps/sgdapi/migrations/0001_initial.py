# Generated by Django 4.0.1 on 2022-01-28 08:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AreaDocumento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255, verbose_name='Nombres de area de documentos')),
            ],
            options={
                'verbose_name': 'AreaDocumento',
                'verbose_name_plural': 'AreaDocumentos',
            },
        ),
        migrations.CreateModel(
            name='Carpeta',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255, verbose_name='Nombres de las carpetas')),
                ('fecha_creacion', models.DateField(auto_now=True, verbose_name='Fecha de Creacion')),
            ],
            options={
                'verbose_name': 'Carpeta',
                'verbose_name_plural': 'Carpetas',
            },
        ),
        migrations.CreateModel(
            name='Contrasena_reinicio',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('correo', models.CharField(max_length=255, verbose_name='Correo usuario')),
                ('token', models.CharField(max_length=255, verbose_name='token validador')),
                ('fecha_cambio', models.DateField(auto_now_add=True, verbose_name='Fecha de Cambio')),
            ],
            options={
                'verbose_name': 'Contrasena_reinicio',
                'verbose_name_plural': 'Contrasenas_reinicios',
            },
        ),
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombreDocumento', models.CharField(max_length=100, verbose_name='Nombres del Usuario')),
                ('fecha_subida', models.DateField(auto_now_add=True, verbose_name='Fecha de subidas')),
                ('extension', models.CharField(max_length=10, verbose_name='Extension de los archivos subidos')),
                ('carpeta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sgdapi.carpeta')),
            ],
            options={
                'verbose_name': 'Documento',
                'verbose_name_plural': 'Documentos',
            },
        ),
        migrations.CreateModel(
            name='SubCarpeta',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombreTipo', models.CharField(max_length=45, verbose_name='Nombres de sub carpetas')),
                ('fecha_creacion', models.DateField(auto_now=True, verbose_name='Fecha de creaciones')),
            ],
            options={
                'verbose_name': 'SubCarpeta',
                'verbose_name_plural': 'SubCarpetas',
            },
        ),
        migrations.CreateModel(
            name='Tipo_carpeta',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombreTipo', models.CharField(max_length=45, verbose_name='Nombres de tipos de carpetas')),
            ],
            options={
                'verbose_name': 'Tipo_carpeta',
                'verbose_name_plural': 'Tipos_carpetas',
            },
        ),
        migrations.CreateModel(
            name='TipoGestion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombres de los tipo de gestiones')),
            ],
            options={
                'verbose_name': 'TipoGestion',
                'verbose_name_plural': 'TiposGestiones',
            },
        ),
        migrations.CreateModel(
            name='UnidadDocumento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255, verbose_name='Nombres de unidad de documentos')),
            ],
            options={
                'verbose_name': 'UnidadDocumento',
                'verbose_name_plural': 'UnidadDocumentos',
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombreUsuario', models.CharField(max_length=255, verbose_name='Nombres del Usuario')),
                ('correo', models.CharField(max_length=255, verbose_name='Correo electronico')),
                ('contrasena', models.CharField(max_length=255, verbose_name='Contraseña')),
                ('avatar', models.CharField(max_length=255, verbose_name='Imagen del usuario')),
                ('estado', models.SmallIntegerField(verbose_name='Estado del usuario')),
                ('fecha_creacion', models.DateField(auto_now_add=True, verbose_name='Fecha de Creacion')),
                ('fecha_actualizacion', models.DateField(auto_now=True, verbose_name='Fecha de Creacion')),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
            },
        ),
        migrations.CreateModel(
            name='PropiedadDocumento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('responsable_doc', models.CharField(max_length=45, verbose_name='Nombres del los responsables')),
                ('areaDocumento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sgdapi.areadocumento')),
                ('unidadDcumento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sgdapi.unidaddocumento')),
            ],
            options={
                'verbose_name': 'PropiedadDocumento',
                'verbose_name_plural': 'PropiedadDocumentos',
            },
        ),
        migrations.CreateModel(
            name='DocumentoOcr',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('contenido', models.TextField(verbose_name='Contenidos del documento')),
                ('fecha_registro', models.DateField(auto_now_add=True, verbose_name='Fecha de registro de converciones')),
                ('documento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sgdapi.documento')),
            ],
            options={
                'verbose_name': 'DocumentoOcr',
                'verbose_name_plural': 'DocumentoOcrs',
            },
        ),
        migrations.AddField(
            model_name='documento',
            name='propiedadDocumento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sgdapi.propiedaddocumento'),
        ),
        migrations.AddField(
            model_name='documento',
            name='tipoGestion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sgdapi.tipogestion'),
        ),
        migrations.AddField(
            model_name='carpeta',
            name='subCarpeta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sgdapi.subcarpeta'),
        ),
        migrations.AddField(
            model_name='carpeta',
            name='tipo_carpeta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sgdapi.tipo_carpeta'),
        ),
    ]
