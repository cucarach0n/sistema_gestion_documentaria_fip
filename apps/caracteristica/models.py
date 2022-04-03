from django.db import models
from simple_history.models import HistoricalRecords
from apps.file.models import File
# Create your models here.
class TipoCaracteristica(models.Model):
    id =models.AutoField(primary_key=True)
    nombreTipo = models.CharField('tipo caracteristica',unique=True,max_length=45,null=False,blank=False)

    class Meta():
        verbose_name = 'Tipo Caracteristica'
        verbose_name_plural = 'Tipo Caracteristicas'
    
    def __str__(self):
        return "{0}".format(self.nombreTipo)

class Caracteristica(models.Model):
    id =models.AutoField(primary_key=True)
    nombreCaracteristica = models.CharField('nombre caracteristica',unique=True,max_length=45,null=False,blank=False)
    tipoCaracteristica = models.ForeignKey(TipoCaracteristica,on_delete=models.CASCADE,null=False,blank=False)
    fechaCreacion = models.DateTimeField("Fecha de creacion",auto_now=True)
    fechaUpdate = models.DateTimeField("Fecha de actualizacion",auto_now_add=True)
    historical = HistoricalRecords(excluded_fields=['nombreCaracteristica','tipoCaracteristica','fechaCreacion','fechaUpdate'])

    @property
    def _history_user(self):
        return self.changed_by
    @_history_user.setter
    def _history_user(self,value):
        self.changed_by = value

    class Meta():
        verbose_name = 'Caracteristica'
        verbose_name_plural = 'Caracteristicas'
    
    def __str__(self):
        return "{0},{1}".format(self.nombreCaracteristica,self.fechaCreacion)

class CaracteristicaFile(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.ForeignKey(File,on_delete=models.CASCADE,null=False,blank=False)
    caracteristica = models.ForeignKey(Caracteristica,on_delete=models.CASCADE,null=False,blank=False)
