from django.db import models
from simple_history.models import HistoricalRecords
from apps.folder.models import Folder
from apps.file.models import File
from apps.users.models import User



# Create your models here.
class FileShare(models.Model):
    id = models.AutoField(primary_key = True)
    file = models.OneToOneField(File,on_delete=models.CASCADE)
    userFrom = models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False,related_name='userFileFrom')
    userTo = models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False,related_name='userFileTo')
    fechaCreacion = models.DateTimeField("Fecha de creacion",auto_now=True)
    fechaUpdate = models.DateTimeField("Fecha de actualizacion",auto_now_add=True)
    estado = models.BooleanField(default = True)
    historical = HistoricalRecords(excluded_fields=['file','userFrom','userTo','fechaCreacion','fechaUpdate','estado',])

    @property
    def _history_user(self):
        return self.changed_by
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value

    class Meta():
        verbose_name = 'FileShare'
        verbose_name_plural = 'FileShares'
    
    def __str__(self):
        return "{0},{1}".format(self.userFrom,self.fechaCreacion)

class FolderShare(models.Model):
    id = models.AutoField(primary_key = True)
    folder = models.OneToOneField(Folder,on_delete=models.CASCADE)
    userFrom = models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False,related_name='userFolderFrom')
    userTo = models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False,related_name='userFolderTo')
    fechaCreacion = models.DateTimeField("Fecha de creacion",auto_now=True)
    fechaUpdate = models.DateTimeField("Fecha de actualizacion",auto_now_add=True)
    estado = models.BooleanField(default = True)
    historical = HistoricalRecords(excluded_fields=['folder','userFrom','userTo','fechaCreacion','fechaUpdate','estado',])

    @property
    def _history_user(self):
        return self.changed_by
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value

    class Meta():
        verbose_name = 'FolderShare'
        verbose_name_plural = 'FolderShares'
    
    def __str__(self):
        return "{0},{1}".format(self.userFrom,self.fechaCreacion)
