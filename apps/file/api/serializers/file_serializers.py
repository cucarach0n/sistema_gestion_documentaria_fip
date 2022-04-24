# -*- coding: utf-8 -*-
from apps.etiqueta.api.serializers.etiqueta_serializers import EtiquetaListSerializer
from apps.etiqueta.models import Etiqueta
from apps.share.models import FileShare, FolderShare
from apps.users.api.serializers.user_serializers import UserFileShareSerializer, UserShareSerializer
from rest_framework import serializers
from apps.file.models import File, FileInFolder, Folder
import os
from django.conf import settings
from apps.base.util import obtenerRuta
from hurry.filesize import size, si
from apps.tag.api.serializers.tag_serializer import TagListSerializer
from apps.tag.models import Tag
from decouple import config
from django.utils.crypto import get_random_string
def crearRutaCompartida(ruta,rutaLogica):
    newRuta = 'Carpeta compartida'
    newrutaLogica = 'Carpeta compartida'
    for i in range(1,len(ruta.split('>'))):
        newRuta += ' > ' + ruta.split('>')[i]
    for i in range(1,len(rutaLogica.split('>'))):
        newrutaLogica += ' > ' + rutaLogica.split('>')[i]
    return newRuta,newrutaLogica
class FileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        exclude = ('extension','slug','contenidoOCR',)
class FileFolderCreateSerializer(serializers.Serializer):
    nombreDocumento = serializers.CharField(max_length=250)
    documento_file = serializers.FileField()
    directorioslug = serializers.CharField(max_length=11)
    #publico = serializers.BooleanField(default = True)
    #unidadareaid = serializers.CharField()

    def validate_nombreDocumento(self,value):
        '''if File.objects.filter(nombreDocumento = value,fileinfolder__parent_folder__slug = self.context['folderSlug']):
            raise serializers.ValidationError("Ya existe un file con este nombre")'''
        if File.objects.filter(nombreDocumento = value,fileinfolder__parent_folder__slug = self.context['folderSlug']):
            return value + "_" + get_random_string(length=3)
        return value

    def create(self,validated_data):
        file = File(nombreDocumento = validated_data['nombreDocumento'],documento_file = validated_data['documento_file'])#,unidadArea_id=validated_data['unidadareaid'])
        file.save()
        return file
class FileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['nombreDocumento']
class FileUpdatePrivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['nombreDocumento','scope']
class FileObtenerSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        exclude = ('extension','documento_file','nombreDocumento','slug','contenidoOCR',)
class FileUpdateOcrSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        exclude = ('documento_file','nombreDocumento','slug','extension','unidadArea','scope','user',)

class FileDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        exclude = ('contenidoOCR','unidadArea',)
    def to_representation(self,instance):
        fileSize = os.path.getsize(settings.MEDIA_ROOT+'files/'+instance.documento_file.name)
        folder = Folder.objects.filter(fileinfolder__file = instance).first()
        fileinfolder = FileInFolder.objects.filter(file = instance).first()
        tag_serializer = TagListSerializer(Tag.objects.filter(filetag__file = instance),many =True)
        etiqueta_serializer = EtiquetaListSerializer(Etiqueta.objects.filter(file = instance),many =True)

        

        if folder:
            '''rutaLogica = "/"+obtenerRuta(folder.id,[folder.nombre],True)+"/"+instance.documento_file.name
            ruta = "/"+obtenerRuta(folder.id,[folder.slug],False)+"/"+instance.slug'''
            rutaLogica = obtenerRuta(folder.id,[folder.nombre],True) +" > "+instance.nombreDocumento
            ruta = obtenerRuta(folder.id,[folder.slug],False)+" > "+instance.slug
        else:
            rutaLogica = "?"
            ruta = "?"
        owner = False
        if instance.user_id == self.context['userId']:
            owner = True
        #print(folder)
        return{
            'nombre':instance.nombreDocumento,
            'nombreArchivo':instance.documento_file.name,
            'owner':owner,
            'slug':instance.slug,
            'size':str(size(fileSize, system=si)),
            'extension':instance.extension,
            'rutaLogica': rutaLogica,
            'rutaSlug':ruta,
            'url':"{0}/file/ver/{1}/".format(config("URL_SERVER"),instance.slug),
            'publico':instance.scope,
            'tags':tag_serializer.data,
            'etiquetas':etiqueta_serializer.data,
            'fechaCreacion':fileinfolder.fechaCreacion,
            'fechaUpdate':fileinfolder.fechaUpdate
        }
class FileDetalleShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        exclude = ('contenidoOCR','unidadArea',)
    def to_representation(self,instance):
        fileSize = os.path.getsize(settings.MEDIA_ROOT+'files/'+instance.documento_file.name)
        folder = Folder.objects.filter(fileinfolder__file = instance).first()
        fileinfolder = FileInFolder.objects.filter(file = instance).first()
        tag_serializer = TagListSerializer(Tag.objects.filter(filetag__file = instance),many =True)
        etiqueta_serializer = EtiquetaListSerializer(Etiqueta.objects.filter(file = instance),many =True)
        if folder:
            '''rutaLogica = "/"+obtenerRuta(folder.id,[folder.nombre],True)+"/"+instance.documento_file.name
            ruta = "/"+obtenerRuta(folder.id,[folder.slug],False)+"/"+instance.slug'''
            rutaLogica = obtenerRuta(folder.id,[folder.nombre],True) +" > "+instance.nombreDocumento
            ruta = obtenerRuta(folder.id,[folder.slug],False)+" > "+instance.slug
            newRuta,newrutaLogica = crearRutaCompartida(ruta,rutaLogica) 
        else:
            rutaLogica = "?"
            ruta = "?"
        fileShareUser = FileShare.objects.filter(userTo_id = self.context['userId'],file_id = instance.id).select_related('userFrom').first()
        if fileShareUser:
            userSerializer = UserFileShareSerializer(fileShareUser).data
        else:
            userSerializer = {}
        #print(folder)
        return{
            'nombre':instance.nombreDocumento,
            'nombreArchivo':instance.documento_file.name,
            'slug':instance.slug,
            'size':str(size(fileSize, system=si)),
            'extension':instance.extension,
            'rutaLogica': newrutaLogica,
            'rutaSlug':newRuta,
            'url':"{0}/file/ver/{1}/".format(config("URL_SERVER"),instance.slug),
            'tags':tag_serializer.data,
            'etiquetas':etiqueta_serializer.data,
            'userFrom':userSerializer,
            'fechaCreacion':fileinfolder.fechaCreacion,
            'fechaUpdate':fileinfolder.fechaUpdate
        }
class FileBuscarSerializer(serializers.Serializer):
    buscar = serializers.CharField(allow_blank=True)
    opcion = serializers.IntegerField()
    def validate_buscar(self,value):
        return value
    def validate(self,data):
        return data
    class Meta:
        model = File
'''class FileHistorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    #history_id = serializers.CharField()
    history_date = serializers.DateTimeField()
    history_change_reason = serializers.CharField()
    history_type = serializers.CharField()
    history_user_id = serializers.IntegerField()'''
class FileBuscarAvanzadoSerializer(serializers.Serializer):
    tipoDoc = serializers.CharField(allow_blank=True)
    nombreDoc = serializers.CharField(allow_blank=True)
    numeroECS=serializers.CharField(allow_blank=True)
    '''numeroCompra=serializers.CharField(allow_blank=True)
    numeroServicio = serializers.CharField(allow_blank=True)'''
    carpetaSlug = serializers.CharField(allow_blank=True)
    fechaInicio = serializers.DateField(allow_null = True)
    fechaFin = serializers.DateField(allow_null = True)
    opcionFecha = serializers.IntegerField(allow_null = True)
    tipoCaracteristicaId = serializers.IntegerField(allow_null = True)
    nombreCaracteristica = serializers.CharField(allow_null = True)
    class Meta:
        model = File


class FileHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = File.historical.model
        fields = ['id','history_date','history_change_reason','history_type','history_user']
    def to_representation(self,instance):
        fileResult = File.objects.filter(id = instance.id).first()
        folderResult = Folder.objects.filter(fileinfolder__file__id = fileResult.id).first()
        return {
            'fileName':fileResult.nombreDocumento,
            'fileSlug':fileResult.slug,
            'rutaLogica': obtenerRuta(folderResult.id,[folderResult.nombre],True),
            'fechaCreacion' : instance.history_date,
            'accion':instance.history_change_reason,
            'tipo':instance.history_type,
            'history_user':instance.history_user.id
        }





    