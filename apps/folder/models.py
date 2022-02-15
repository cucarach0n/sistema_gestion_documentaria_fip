from django.db import models
from simple_history.models import HistoricalRecords

# Create your models here.
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