from django.contrib import admin
from apps.sgdapi.models import *

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id','nombreUsuario','correo','password','avatar','estado','fechaCreacion','fechaActualizacion')

class Contrasena_reinicioAdmin(admin.ModelAdmin):
    list_display = ('id','correo','token','fechaCambio','estado')

#class Contrasena_reinicioAdmin(admin.ModelAdmin):
#    list_display = ('id','correo','token','fechaCambio','estado')
# Register your models here.
admin.site.register(Usuario,UsuarioAdmin)
admin.site.register(Contrasena_reinicio,Contrasena_reinicioAdmin)
admin.site.register(TipoGestion)
admin.site.register(Tipo_carpeta)
admin.site.register(SubCarpeta)
admin.site.register(UnidadDocumento)
admin.site.register(AreaDocumento)
admin.site.register(Carpeta)
admin.site.register(PropiedadDocumento)
admin.site.register(Documento)
admin.site.register(DocumentoOcr)
