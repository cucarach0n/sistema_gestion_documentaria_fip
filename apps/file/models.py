# -*- coding: utf-8 -*-
from django.db import models
from apps.users.models import User
from simple_history.models import HistoricalRecords

from apps.tag.models import Tag
from apps.folder.models import Folder
# Create your models here.
from apps.unidadArea.models import UnidadArea


class File(models.Model):
    id = models.AutoField(primary_key = True)
    slug = models.CharField('Sulg',max_length=11,null = False, blank = False)
    nombreDocumento = models.CharField('Nombres del documento',max_length=250,null = False, blank = False)
    contenidoOCR = models.TextField('Contenidos del documento', null = True, blank = True)
    documento_file = models.FileField('Archivo del documento', upload_to="",blank = False,null = False)
    extension = models.CharField('Extension de los archivos subidos',max_length=20,null = True, blank = True)
    unidadArea = models.ForeignKey(UnidadArea,on_delete = models.CASCADE,null=True,blank=True)
    scope = models.BooleanField(default = True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False)
    eliminado = models.BooleanField(default = False)
    historical = HistoricalRecords(excluded_fields=['slug','contenidoOCR','documento_file','extension','unidadArea','user','scope',])

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



class FileInFolder(models.Model):
    id =models.AutoField(primary_key=True)
    parent_folder = models.ForeignKey(Folder,on_delete = models.CASCADE)
    file = models.ForeignKey('File',on_delete = models.CASCADE)
    fechaCreacion = models.DateTimeField("Fecha de creacion",auto_now=True)
    fechaUpdate = models.DateTimeField("Fecha de actualizacion",auto_now_add=True)

    historical = HistoricalRecords(excluded_fields=['parent_folder','file','fechaCreacion','fechaUpdate',])

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
    tag = models.ForeignKey(Tag,on_delete = models.CASCADE)
    file = models.ForeignKey('File',on_delete = models.CASCADE,related_name='filetag')
    fechaRegistro = models.DateTimeField("Fecha del registro",auto_now=True)
    fechaUpdate = models.DateTimeField("Fecha del registro",auto_now_add=True)

    historical = HistoricalRecords(excluded_fields=['tag','file','fechaRegistro','fechaUpdate',])

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
class FileTrash(models.Model):
    id =models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    file = models.ForeignKey(File,on_delete = models.CASCADE)
    fechaEliminacion = models.DateTimeField("Fecha de creacion",auto_now=True)
    fechaUpdate = models.DateTimeField("Fecha de actualizacion",auto_now_add=True)

    historical = HistoricalRecords()
    
    @property
    def _history_user(self):
        return self.changed_by
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value

    class Meta():
        verbose_name = 'Folder trash'
        verbose_name_plural = 'Folder trashs'
    
    def __str__(self):
        return "{0},{1}".format(self.user,self.fechaEliminacion)