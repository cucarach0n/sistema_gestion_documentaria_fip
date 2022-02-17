from django.contrib import admin
from apps.file.models import *



class Contrasena_reinicioAdmin(admin.ModelAdmin):
    list_display = ('id','correo','token','fechaCambio','estado')

#class Contrasena_reinicioAdmin(admin.ModelAdmin):
#    list_display = ('id','correo','token','fechaCambio','estado')
# Register your models here.
#admin.site.register(Contrasena_reinicio,Contrasena_reinicioAdmin)
#admin.site.register(Tag)
#admin.site.register(Folder)
#admin.site.register(FolderInFolder)
admin.site.register(File)
admin.site.register(FileInFolder)
admin.site.register(FileTag)
