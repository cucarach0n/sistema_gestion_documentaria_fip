from apps.folder.models import FolderInFolder
from apps.unidadArea.models import UnidadArea
from rest_framework import serializers
from apps.file.models import File, FileInFolder, Folder
import os
from django.conf import settings
from apps.base.util import obtenerRuta
from hurry.filesize import size, si
from apps.tag.api.serializers.tag_serializer import TagListSerializer
from apps.tag.models import Tag
class FileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        exclude = ('extension','slug','contenidoOCR',)
class FileFolderCreateSerializer(serializers.Serializer):
    nombreDocumento = serializers.CharField(max_length=50)
    documento_file = serializers.FileField()
    directorioslug = serializers.CharField(max_length=11)
    #unidadareaid = serializers.CharField()

    

    def create(self,validated_data):
        file = File(nombreDocumento = validated_data['nombreDocumento'],documento_file = validated_data['documento_file'])#,unidadArea_id=validated_data['unidadareaid'])
        file.save()
        return file

class FileObtenerSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        exclude = ('extension','documento_file','nombreDocumento','slug','contenidoOCR',)
class FileUpdateOcrSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        exclude = ('extension','documento_file','nombreDocumento','slug',)

class FileDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        exclude = ('contenidoOCR','unidadArea',)
    def to_representation(self,instance):
        fileSize = os.path.getsize(settings.MEDIA_ROOT+'files/'+instance.documento_file.name)
        folder = Folder.objects.filter(fileinfolder__file = instance).first()
        fileinfolder = FileInFolder.objects.filter(file = instance).first()
        tag_serializer = TagListSerializer(Tag.objects.filter(filetag__file = instance),many =True)
        if folder:
            '''rutaLogica = "/"+obtenerRuta(folder.id,[folder.nombre],True)+"/"+instance.documento_file.name
            ruta = "/"+obtenerRuta(folder.id,[folder.slug],False)+"/"+instance.slug'''
            rutaLogica = obtenerRuta(folder.id,[folder.nombre],True)
            ruta = "/"+obtenerRuta(folder.id,[folder.slug],False)+"/"+instance.slug
        else:
            rutaLogica = "?"
            ruta = "?"
        
        print(folder)
        return{
            'nombre':instance.nombreDocumento,
            'nombreArchivo':instance.documento_file.name,
            'slug':instance.slug,
            'size':str(size(fileSize, system=si)),
            'extension':instance.extension,
            'rutaLogica': rutaLogica,
            'rutaSlug':ruta,
            'url':"https://localhost:8000/sgdapi/ver/"+instance.slug+"/",
            'tags':tag_serializer.data,
            'fechaCreacion':fileinfolder.fechaCreacion,
            'fechaUpdate':fileinfolder.fechaUpdate
        }
class FileBuscarSerializer(serializers.Serializer):
    buscar = serializers.CharField(allow_blank=True)

    def validate_buscar(self,value):
        return value
    def validate(self,data):
        return data
    class Meta:
        model = File





    