from django.db import models
from simple_history.models import HistoricalRecords
from apps.users.models import User
from apps.file.models import File
# Create your models here.
class Etiqueta(models.Model):
    id =models.AutoField(primary_key=True)
    nombre = models.CharField('Nombre de la etiqueta',max_length=45,null=False,blank=False)
    file = models.ForeignKey(File,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
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
        verbose_name = 'Etiqueta'
        verbose_name_plural = 'Etiquetas'
    
    def __str__(self):
        return "{0},{1}".format(self.nombre,self.fechaCreacion)