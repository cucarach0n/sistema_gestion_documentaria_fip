from django.contrib import admin

from apps.caracteristica.models import Caracteristica, CaracteristicaFile, TipoCaracteristica

# Register your models here.
admin.site.register(TipoCaracteristica)
admin.site.register(Caracteristica)
admin.site.register(CaracteristicaFile)