from rest_framework import serializers
from apps.folder.models import Folder,FolderInFolder
from apps.base.util import obtenerRuta

class TreeFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = '__all__'

    def to_representation(self,instance):
        #ruta = obtenerRuta(instance.id,[instance.slug],False)
        #rutaLogica = obtenerRuta(instance.id,[instance.nombre],True)
        return {
            
            'slug':instance.slug,
            'nombre':instance.nombre,
            #'rutaFisica':"/"+rutaLogica,
            #'rutaSlug':"/"+ruta,
            #'fechaCreacion':instance.fechaCreacion,
            #'fechaUpdate':instance.fechaUpdate
            'isFolder':True,
            'isFolderMaster':False,
            'isStartFolder':False,
            'folders':[]
        }