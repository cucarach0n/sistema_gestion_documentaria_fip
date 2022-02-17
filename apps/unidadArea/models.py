from django.db import models
from simple_history.models import HistoricalRecords

# Create your models here.
class UnidadArea(models.Model):
    id = models.AutoField(primary_key=True)
    nombreUnidad = models.CharField("Nombre del unidad",max_length=100,unique=True,null=False,blank=False)
    fechaRegistro = models.DateTimeField("Fecha del registro",auto_now=True)
    fechaUpdate = models.DateTimeField("Fecha del registro",auto_now_add=True)

    '''historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value'''

    class Meta():
        verbose_name = 'Unidad Area'
        verbose_name_plural = 'Unidad Areas'
    
    def __str__(self):
        return "{0},{1}".format(self.nombreUnidad,self.fechaUpdate)