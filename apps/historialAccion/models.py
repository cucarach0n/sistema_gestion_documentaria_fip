from django.db import models
from simple_history.models import HistoricalRecords
# Create your models here.


class tipoAccion(models.Model):
    id = models.AutoField(primary_key = True)
    nombreDocumento = models.CharField('Nombres de la accion',max_length=150,null = False, blank = False)
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
        verbose_name = 'tipoAccion'
        verbose_name_plural = 'tipoAcciones'
    
    def __str__(self):
        return "{0},{1}".format(self.id,self.nombreDocumento)

class historialAccion(models.Model):
    id = models.AutoField(primary_key = True)
    nombreTabla = models.CharField('Nombre de la tabla',max_length=150,null = False, blank = False)
    identificadorRegistro = models.CharField('Nombre de la tabla',max_length=100,null = False, blank = False)
    tipoAccion = models.ForeignKey(tipoAccion,on_delete=models.CASCADE,null=False,blank=False)
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
        verbose_name = 'File'
        verbose_name_plural = 'Files'
    
    def __str__(self):
        return "{0},{1}".format(self.nombreDocumento,self.slug)