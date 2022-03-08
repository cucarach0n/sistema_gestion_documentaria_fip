from django.db import models
from simple_history.models import HistoricalRecords

# Create your models here.
class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    tagName = models.CharField("Nombre del tag",max_length=50,unique=True,null=False,blank=False)
    fechaRegistro = models.DateTimeField("Fecha del registro",auto_now=True)
    fechaUpdate = models.DateTimeField("Fecha del registro",auto_now=False,auto_now_add=True)
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