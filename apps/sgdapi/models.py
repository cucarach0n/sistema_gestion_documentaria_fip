from hashlib import blake2b
from pyexpat import model
from statistics import mode
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from simple_history.models import HistoricalRecords
# Create your models here.

class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    tagName = models.CharField("Nombre del tag",max_length=50,unique=True,null=False,blank=False)
    fechaRegistro = models.DateTimeField("Fecha del registro",auto_now=True)
    fechaUpdate = models.DateTimeField("Fecha del registro",auto_now_add=True)

    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value

    class Meta():
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
    
    def __str__(self):
        return "{0},{1}".format(self.tagName,self.fechaRegistro)

class Folder(models.Model):
    id =models.AutoField(primary_key=True)
    slug = models.CharField('Slug',unique=True,max_length=6,null=False,blank=False)
    nombre = models.CharField('Nombre del folder',max_length=45,null=False,blank=False)
    fechaCreacion = models.DateTimeField("Fecha de creacion",auto_now=True)
    fechaUpdate = models.DateTimeField("Fecha de actualizacion",auto_now_add=True)

    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value

    class Meta():
        verbose_name = 'Folder'
        verbose_name_plural = 'Folders'
    
    def __str__(self):
        return "{0},{1}".format(self.nombre,self.slug)

class FolderInFolder(models.Model):
    id =models.AutoField(primary_key=True)
    child_folder_name = models.CharField('Nombre del folder Hijo',max_length=45,null=False,blank=False)
    parent_folder = models.ForeignKey('Folder',on_delete = models.CASCADE,related_name='carpeta_padre')
    child_folder = models.ForeignKey('Folder',on_delete = models.CASCADE,related_name='carpeta_hija')
    fechaCreacion = models.DateTimeField("Fecha de creacion",auto_now=True)
    fechaUpdate = models.DateTimeField("Fecha de actualizacion",auto_now_add=True)

    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value

    class Meta():
        verbose_name = 'Folder en folder'
        verbose_name_plural = 'Folder en folders'
    
    def __str__(self):
        return "{0},{1}".format(self.child_folder_name,self.slug)

class File(models.Model):
    id = models.AutoField(primary_key = True)
    slug = models.CharField('Sulg',max_length=6,null = False, blank = False)
    nombreDocumento = models.CharField('Nombres del documento',max_length=100,null = False, blank = False)
    contenidoOCR = models.TextField('Contenidos del documento', null = False, blank = False)
    documento_file = models.FileField('Archivo del documento', upload_to="",blank = True,null = True)
    extension = models.CharField('Extension de los archivos subidos',max_length=10,null = True, blank = True)

    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value

    class Meta():
        verbose_name = 'File'
        verbose_name_plural = 'Files'
    
    def __str__(self):
        return "{0},{1}".format(self.nombreDocumento,self.slug)

class UnidadArea(models.Model):
    id = models.AutoField(primary_key=True)
    nombreUnidad = models.CharField("Nombre del unidad",max_length=100,unique=True,null=False,blank=False)
    file = models.ForeignKey('File',on_delete = models.CASCADE)
    fechaRegistro = models.DateTimeField("Fecha del registro",auto_now=True)
    fechaUpdate = models.DateTimeField("Fecha del registro",auto_now_add=True)

    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value

    class Meta():
        verbose_name = 'Unidad Area'
        verbose_name_plural = 'Unidad Areas'
    
    def __str__(self):
        return "{0},{1}".format(self.nombreUnidad,self.fechaUpdate)


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

class FileInFolder(models.Model):
    id =models.AutoField(primary_key=True)
    parent_folder = models.ForeignKey('Folder',on_delete = models.CASCADE)
    file = models.ForeignKey('File',on_delete = models.CASCADE)
    fechaCreacion = models.DateTimeField("Fecha de creacion",auto_now=True)
    fechaUpdate = models.DateTimeField("Fecha de actualizacion",auto_now_add=True)

    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value

    class Meta():
        verbose_name = 'File en folder'
        verbose_name_plural = 'Files en folders'
    
    def __str__(self):
        return "{0},{1}".format(self.slug,self.fechaUpdate)


class FileTag(models.Model):

    id = models.AutoField(primary_key=True)
    tag = models.ForeignKey('Tag',on_delete = models.CASCADE)
    file = models.ForeignKey('File',on_delete = models.CASCADE)
    fechaRegistro = models.DateTimeField("Fecha del registro",auto_now=True)
    fechaUpdate = models.DateTimeField("Fecha del registro",auto_now_add=True)

    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value

    class Meta():
        verbose_name = 'File Tag'
        verbose_name_plural = 'File Tags'
    
    def __str__(self):
        return "{0},{1}".format(self.id,self.fechaUpdate)