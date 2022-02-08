from hashlib import blake2b
from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from simple_history.models import HistoricalRecords
# Create your models here.

class Usuario(AbstractBaseUser,models.Model):
    id = models.AutoField(primary_key = True)
    nombreUsuario = models.CharField('Nombres del Usuario',max_length=255,null = False, blank = False, unique=True)
    correo = models.EmailField('Correo electronico',max_length=255,null = False, blank = False, unique=True)
    password = models.CharField('Contraseña',max_length=100,null = False, blank = False)
    avatar = models.ImageField('Imagen del usuario',upload_to='avatars/', blank = True, null= True)
    estado = models.SmallIntegerField('Estado del usuario',null = True, default=0, blank = False)
    fechaCreacion = models.DateTimeField('Fecha de Creacion',auto_now = True,auto_now_add = False) 
    fechaActualizacion = models.DateTimeField('Fecha de actualizacion',auto_now = False,auto_now_add = True)
    class Meta():
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return "{0},{1}".format(self.nombreUsuario,self.fechaCreacion)


class Contrasena_reinicio(models.Model):
    id = models.AutoField(primary_key = True)
    correo = models.EmailField('Correo usuario',max_length=255,null = False, blank = False, unique=True)
    token = models.CharField('token validador',max_length=40,null = False, blank = False, unique=True)
    fechaCambio = models.DateTimeField('Fecha de Cambio',auto_now = False,auto_now_add = True) 
    estado = models.SmallIntegerField('Estado del token',null = True, default=1, blank = False)
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value

    class Meta():
        verbose_name = 'Contrasena_reinicio'
        verbose_name_plural = 'Contrasenas_reinicios'
    
    def __str__(self):
        return "{0},{1}".format(self.correo,self.fechaCambio)

class TipoGestion(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField('Nombres de los tipo de gestiones',max_length=100,null = False, blank = False)
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value

    class Meta():
        verbose_name = 'TipoGestion'
        verbose_name_plural = 'TiposGestiones'
    
    def __str__(self):
        return "{0},{1}".format(self.id,self.nombre)


class Tipo_carpeta(models.Model):
    id = models.AutoField(primary_key = True)
    nombreTipo = models.CharField('Nombres de tipos de carpetas',max_length=45,null = False, blank = False)
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value

    class Meta():
        verbose_name = 'Tipo_carpeta'
        verbose_name_plural = 'Tipos_carpetas'
    
    def __str__(self):
        return "{0},{1}".format(self.id,self.nombreTipo)


class SubCarpeta(models.Model):
    id = models.AutoField(primary_key = True)
    nombreTipo = models.CharField('Nombres de sub carpetas',max_length=45,null = False, blank = False)
    fechaCreacion = models.DateTimeField('Fecha de creaciones',auto_now = True,auto_now_add = False) 
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value

    class Meta():
        verbose_name = 'SubCarpeta'
        verbose_name_plural = 'SubCarpetas'
    
    def __str__(self):
        return "{0},{1}".format(self.nombreTipo,self.fecha_creacion)

class UnidadDocumento(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField('Nombres de unidad de documentos',max_length=255,null = False, blank = False)
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value

    class Meta():
        verbose_name = 'UnidadDocumento'
        verbose_name_plural = 'UnidadDocumentos'
    
    def __str__(self):
        return "{0},{1}".format(self.id,self.nombre)

class AreaDocumento(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField('Nombres de area de documentos',max_length=255,null = False, blank = False)
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value

    class Meta():
        verbose_name = 'AreaDocumento'
        verbose_name_plural = 'AreaDocumentos'
    
    def __str__(self):
        return "{0},{1}".format(self.id,self.nombre)

class Carpeta(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField('Nombres de las carpetas',max_length=255,null = False, blank = False)
    fechaCreacion = models.DateTimeField('Fecha de Creacion',auto_now = True,auto_now_add = False) 
    tipoCarpeta = models.ForeignKey('Tipo_carpeta',on_delete = models.CASCADE)
    subCarpeta = models.ForeignKey('SubCarpeta',on_delete = models.CASCADE)
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value

    class Meta():
        verbose_name = 'Carpeta'
        verbose_name_plural = 'Carpetas'
    
    def __str__(self):
        return "{0},{1}".format(self.id,self.nombre)


class PropiedadDocumento(models.Model):
    id = models.AutoField(primary_key = True)
    responsableDoc = models.CharField('Nombres del los responsables',max_length=45,null = False, blank = False)
    unidadDcumento = models.ForeignKey('UnidadDocumento',on_delete = models.CASCADE)
    areaDocumento = models.ForeignKey('AreaDocumento',on_delete = models.CASCADE)
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value

    class Meta():
        verbose_name = 'PropiedadDocumento'
        verbose_name_plural = 'PropiedadDocumentos'
    
    def __str__(self):
        return "{0},{1}".format(self.id,self.responsable_doc)

class Documento(models.Model):
    id = models.AutoField(primary_key = True)
    documento_file = models.FileField('Archivo del documento', upload_to="",blank = True,null = True)
    nombreDocumento = models.CharField('Nombres del documento',max_length=100,null = False, blank = False)
    fechaSubida = models.DateTimeField('Fecha de subidas',auto_now = False,auto_now_add = True,null = False, blank = False) 
    extension = models.CharField('Extension de los archivos subidos',max_length=10,null = True, blank = True)
    '''
    carpeta = models.ForeignKey('Carpeta',on_delete = models.CASCADE)
    propiedadDocumento = models.ForeignKey('PropiedadDocumento',on_delete = models.CASCADE)
    tipoGestion = models.ForeignKey('TipoGestion',on_delete = models.CASCADE)
    '''
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value

    class Meta():
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'
    
    def __str__(self):
        return "{0},{1}".format(self.id,self.nombreDocumento)

class DocumentoOcr(models.Model):
    id = models.AutoField(primary_key = True)
    contenido = models.TextField('Contenidos del documento', null = False, blank = False)
    fechaRegistro = models.DateTimeField('Fecha de registro de converciones',auto_now = False,auto_now_add = True) 
    documento = models.ForeignKey('Documento',on_delete = models.CASCADE)
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value


    class Meta():
        verbose_name = 'DocumentoOcr'
        verbose_name_plural = 'DocumentoOcrs'
    
    def __str__(self):
        return "{0},{1}".format(self.id,self.fecha_registro)
