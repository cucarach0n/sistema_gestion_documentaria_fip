from rest_framework import serializers
from apps.sgdapi.models import File, Folder
import os
from django.conf import settings
from apps.sgdapi.util import obtenerRuta

class FileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        exclude = ('extension','slug','contenidoOCR',)
class FileFolderCreateSerializer(serializers.Serializer):
    nombreDocumento = serializers.CharField(max_length=50)
    documento_file = serializers.FileField()
    directorioslug = serializers.CharField(max_length=6)

    def create(self,validated_data):
        file = File(nombreDocumento = validated_data['nombreDocumento'],documento_file = validated_data['documento_file'])
        file.save()
        return file

class FileObtenerSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        exclude = ('extension','documento_file','nombreDocumento','slug','contenidoOCR',)

class FileDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        exclude = ('contenidoOCR',)
    def to_representation(self,instance):
        size = os.path.getsize(settings.MEDIA_ROOT+'files/'+instance.documento_file.name)
        folder = Folder.objects.filter(fileinfolder__file = instance).first()
        if folder:
            rutaLogica = obtenerRuta(folder.id,[folder.nombre],True)+"/"+instance.documento_file.name
            ruta = obtenerRuta(folder.id,[folder.slug],False)+"/"+instance.slug
        else:
            rutaLogica = "#"
            ruta = "#"
            instance.slug = "#"
        return{
            'nombre':instance.nombreDocumento,
            'nombreArchivo':instance.documento_file.name,
            'slug':instance.slug,
            'size':size,
            'extension':instance.extension,
            'rutaLogica': "/"+rutaLogica,
            'rutaSlug':"/"+ruta,
            'url':"http://localhost:8000/documento/ver/"+instance.slug+"/",
        }

    

    