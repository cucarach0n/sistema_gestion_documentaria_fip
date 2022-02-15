from rest_framework import serializers
from apps.sgdapi.models import Folder,FolderInFolder,File
from apps.sgdapi.api.serializers.documento_serializers import FileDetalleSerializer
from apps.sgdapi.util import obtenerRuta

class FolderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = '__all__'

    def to_representation(self,instance):
        ruta = obtenerRuta(instance.id,[instance.slug],False)
        rutaLogica = obtenerRuta(instance.id,[instance.nombre],True)
        return {
            
            'slug':instance.slug,
            'nombre':instance.nombre,
            'rutaFisica':"/"+rutaLogica,
            'rutaSlug':"/"+ruta,
            'fechaCreacion':instance.fechaCreacion,
            'fechaUpdate':instance.fechaUpdate
        }

class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        exclude = ('id','fechaUpdate','fechaCreacion','slug')
    def validate_nombre(self,value):
        print(value)
        if Folder.objects.filter(nombre = value):    
            folders = FolderInFolder.objects.filter(child_folder_id = Folder.objects.filter(nombre = value).first())
            if folders is None:
                return value
            else:
                raise serializers.ValidationError('Error, ya existe este directorio')  
        else:
            return value
            

    def validate(self,data):
        return data
class FolderList2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        exclude =('id',)
class FolderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        exclude = ('slug',)
    def validate_nombre(self,value):
        print(value)  
        print(self.context.id)
        folders = FolderInFolder.objects.filter(child_folder_name = value,parent_folder_id = self.context.id).first()
        print(folders)
        if folders is None:
            return value
        else:
            raise serializers.ValidationError('Error, ya existe este directorio en la carpeta raiz')  

            

    def validate(self,data):
        return data

class FolderListaEnlasada():
    lista = []
    def addLista(self,Objeto):
        self.lista.append(Objeto)
    def getLista(self):
        return self.lista
    def __init__(self, id = None, slug = None, nombre = None, fechaCreacion = None, fechaUpdate = None):
        self.id = id
        self.slug = slug
        self.nombre = nombre
        self.fechaCreacion = fechaCreacion
        self.fechaUpdate = fechaUpdate


class FolderDirecotorioListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Folder
        fields = "__all__"
    def to_representation(self,instance):
        
        folder = FolderDetailSerializer(Folder.objects.filter(carpeta_hija__parent_folder_id = instance.id),many = True)
        files = FileDetalleSerializer(File.objects.filter(fileinfolder__parent_folder__id =instance.id),many = True,context = {'padre':instance.id})
        ruta = obtenerRuta(instance.id,[instance.slug],False)
        rutaLogica = obtenerRuta(instance.id,[instance.nombre],True)
        
        return {
            'slug':instance.slug,
            'nombre':instance.nombre,
            'rutaLogica': "/"+rutaLogica,
            'rutaSlug': "/"+ruta,
            'fechaCreacion':instance.fechaCreacion,
            'fechaUpdate':instance.fechaUpdate,
            'subdirectorios': folder.data,
            'files':files.data
        }





