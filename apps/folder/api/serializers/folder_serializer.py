from apps.share.models import FolderShare
from apps.users.api.serializers.user_serializers import UserShareSerializer
from rest_framework import serializers
from apps.folder.models import Folder,FolderInFolder
from apps.file.models import File
from apps.file.api.serializers.file_serializers import FileDetalleSerializer, FileDetalleShareSerializer
from apps.base.util import obtenerRuta
from apps.folder.api.serializers.treefolder_serializer import TreeFolderSerializer
from django.db.models import Q

def crearRutaCompartida(ruta,rutaLogica,newNameFolder = "Carpeta compartida"):
    newRuta = newNameFolder
    newrutaLogica = newNameFolder
    for i in range(1,len(ruta.split('>'))):
        newRuta += ' > ' + ruta.split('>')[i]
    for i in range(1,len(rutaLogica.split('>'))):
        newrutaLogica += ' > ' + rutaLogica.split('>')[i]
    return newRuta,newrutaLogica

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
            'rutaFisica':rutaLogica,
            'rutaSlug':"/"+ruta,
            'fechaCreacion':instance.fechaCreacion,
            'fechaUpdate':instance.fechaUpdate,
            'publico':instance.scope
        }
class FolderDetailShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = '__all__'

    def to_representation(self,instance):
        ruta = obtenerRuta(instance.id,[instance.slug],False)
        rutaLogica = obtenerRuta(instance.id,[instance.nombre],True)
        newRuta,newrutaLogica = crearRutaCompartida(ruta,rutaLogica) 
        return {
            
            'slug':instance.slug,
            'nombre':instance.nombre,
            'rutaFisica':newrutaLogica,
            'rutaSlug':"/"+newRuta,
            'fechaCreacion':instance.fechaCreacion,
            'fechaUpdate':instance.fechaUpdate
        }
class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        exclude = ('id','fechaUpdate','fechaCreacion','slug','user',)
    def validate_nombre(self,value):
        #print(value)
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
        exclude = ('slug','user',)
    def validate_nombre(self,value):
        #print(value)  
        #print(self.context.id)
        folders = FolderInFolder.objects.filter(child_folder_name = value,parent_folder_id = self.context.id).first()
        #print(folders)
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
        #test
        #fol = Folder.objects.filter(Q(user_id = self.context['userId'],scope=False,carpeta_hija__parent_folder_id = instance.id) | Q(scope = True,carpeta_hija__parent_folder_id = instance.id)).distinct()
        #print(Folder.objects.filter(carpeta_hija__parent_folder_id = instance.id))
        #print(self.context['userId'])
        #print(fol)
        #fintest
        #backup
        '''folder = FolderDetailSerializer(Folder.objects.filter(carpeta_hija__parent_folder_id = instance.id),many = True)'''
        #endbackup
        if int(self.context['userStaff']) < 3: 
            #V1
            '''folderQuery = Folder.objects.filter(Q(user_id = self.context['userId'],scope=False,carpeta_hija__parent_folder_id = instance.id) 
                                                | Q(scope = True,carpeta_hija__parent_folder_id = instance.id)).distinct()
            fileQuery = File.objects.filter(Q(user_id = self.context['userId'],scope = False,fileinfolder__parent_folder__id =instance.id)
                                            |Q(scope = True,fileinfolder__parent_folder__id =instance.id)).distinct()'''
            #V2
            '''folderQuery = Folder.objects.filter(scope = True,carpeta_hija__parent_folder_id = instance.id)
            fileQuery = File.objects.filter(scope = True,fileinfolder__parent_folder__id =instance.id)'''
            #V3
            folderQuery = Folder.objects.filter(Q(scope = False,carpeta_hija__parent_folder_id = instance.id,user_id = self.context['userId'],eliminado = False)|
                                                Q(scope = True,carpeta_hija__parent_folder_id = instance.id,eliminado = False))
            fileQuery = File.objects.filter(Q(scope = False,fileinfolder__parent_folder__id =instance.id,user_id = self.context['userId'],eliminado = False)|
                                            Q(scope = True,fileinfolder__parent_folder__id =instance.id,eliminado = False))                              
        elif int(self.context['userStaff']) > 2 and int(self.context['userStaff']) < 5:
            
            folderQuery = Folder.objects.filter(carpeta_hija__parent_folder_id = instance.id)
            fileQuery = File.objects.filter(fileinfolder__parent_folder__id =instance.id)
        #carpetas compartidas
        elif int(self.context['userStaff']) == 5:
            
            folderQuery = Folder.objects.filter(scope = True,carpeta_hija__parent_folder_id = instance.id)
            fileQuery = File.objects.filter(scope = True,fileinfolder__parent_folder__id =instance.id)
        '''elif int(self.context['userStaff']) == 6:
            
            folderQuery = Folder.objects.filter(scope = False,carpeta_hija__parent_folder_id = instance.id,user_id = self.context['userId'])
            fileQuery = File.objects.filter(scope = False,fileinfolder__parent_folder__id =instance.id,user_id = self.context['userId'])'''

        folder = FolderDetailSerializer(folderQuery,many = True)
        #files = FileDetalleSerializer(File.objects.filter(fileinfolder__parent_folder__id =instance.id),many = True,context = {'padre':instance.id})
        files = FileDetalleSerializer(fileQuery,many = True,context = {'padre':instance.id})
        ruta = obtenerRuta(instance.id,[instance.slug],False)
        rutaLogica = obtenerRuta(instance.id,[instance.nombre],True)
        #treeArbolSerializer = TreeFolderSerializer(Folder.objects.filter(carpeta_hija__parent_folder_id = instance.id),many = True)
        treeArbolSerializer = TreeFolderSerializer(folderQuery,many = True)
        return {
            'slug':instance.slug,
            'nombre':instance.nombre,
            'rutaLogica': rutaLogica,
            'rutaSlug': "/"+ruta,
            'fechaCreacion':instance.fechaCreacion,
            'fechaUpdate':instance.fechaUpdate,
            'publico':instance.scope,
            'subdirectorios': folder.data,
            'files':files.data,
            'treefolders':treeArbolSerializer.data
        }
class FolderDirecotorioListShareSerializer(serializers.ModelSerializer):

    class Meta:
        model = Folder
        fields = "__all__"
    def to_representation(self,instance):
        folderQuery = Folder.objects.filter(scope = True,carpeta_hija__parent_folder_id = instance.id,eliminado = False)
        fileQuery = File.objects.filter(scope = True,fileinfolder__parent_folder__id =instance.id,eliminado = False)


        folder = FolderDetailShareSerializer(folderQuery,many = True)
        files = FileDetalleShareSerializer(fileQuery,many = True,context = {'userId':self.context['userId']})
        ruta = obtenerRuta(instance.id,[instance.slug],False)
        rutaLogica = obtenerRuta(instance.id,[instance.nombre],True)
        newRuta,newrutaLogica = crearRutaCompartida(ruta,rutaLogica) 
        treeArbolSerializer = TreeFolderSerializer(folderQuery,many = True)

        folderShareUser = FolderShare.objects.filter(userTo_id = self.context['userId'],folder_id = instance.id).select_related('userFrom').first()
        if folderShareUser:
            userSerializer = UserShareSerializer(folderShareUser).data
        else:
            userSerializer = {}
        return {
            'slug':instance.slug,
            'nombre':instance.nombre,
            'rutaLogica': newrutaLogica.replace('  '," "),
            'rutaSlug': newRuta.replace('  '," "),
            'fechaCreacion':instance.fechaCreacion,
            'fechaUpdate':instance.fechaUpdate,
            'subdirectorios': folder.data,
            'files':files.data,
            'userFrom':userSerializer,
            'treefolders':treeArbolSerializer.data
        }
class FolderTrashListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Folder
        fields = "__all__"
    def to_representation(self,instance):
        folderQuery = Folder.objects.filter(scope = False,carpeta_hija__parent_folder_id = instance.id,eliminado =True)
        fileQuery = File.objects.filter(scope = False,fileinfolder__parent_folder__id =instance.id,eliminado =True)

        folder = FolderDetailShareSerializer(folderQuery,many = True)
        files = FileDetalleSerializer(fileQuery,many = True,context = {'padre':instance.id})
        ruta = obtenerRuta(instance.id,[instance.slug],False)
        rutaLogica = obtenerRuta(instance.id,[instance.nombre],True)
        newRuta,newrutaLogica = crearRutaCompartida(ruta,rutaLogica,'Papelera Privada') 
        treeArbolSerializer = TreeFolderSerializer(folderQuery,many = True)
        return {
            'slug':instance.slug,
            'nombre':instance.nombre,
            'rutaLogica': newrutaLogica.replace('  '," "),
            'rutaSlug': newRuta.replace('  '," "),
            'fechaCreacion':instance.fechaCreacion,
            'fechaUpdate':instance.fechaUpdate,
            'subdirectorios': folder.data,
            'files':files.data,
            'treefolders':treeArbolSerializer.data
        }
class FolderTrashPublicListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Folder
        fields = "__all__"
    def to_representation(self,instance):
        folderQuery = Folder.objects.filter(scope = True,carpeta_hija__parent_folder_id = instance.id,eliminado =True)
        fileQuery = File.objects.filter(scope = True,fileinfolder__parent_folder__id =instance.id,eliminado =True)

        folder = FolderDetailShareSerializer(folderQuery,many = True)
        files = FileDetalleSerializer(fileQuery,many = True,context = {'padre':instance.id})
        ruta = obtenerRuta(instance.id,[instance.slug],False)
        rutaLogica = obtenerRuta(instance.id,[instance.nombre],True)
        newRuta,newrutaLogica = crearRutaCompartida(ruta,rutaLogica,'Papelera Publica') 
        treeArbolSerializer = TreeFolderSerializer(folderQuery,many = True)
        return {
            'slug':instance.slug,
            'nombre':instance.nombre,
            'rutaLogica': newrutaLogica.replace('  '," "),
            'rutaSlug': newRuta.replace('  '," "),
            'fechaCreacion':instance.fechaCreacion,
            'fechaUpdate':instance.fechaUpdate,
            'subdirectorios': folder.data,
            'files':files.data,
            'treefolders':treeArbolSerializer.data
        }
class FolderDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = "__all__"
class FolderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ['nombre']
class FolderUpdatePrivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ['nombre','scope']

class FolderHistoryTestSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    #history_id = serializers.CharField()
    history_date = serializers.DateTimeField()
    history_change_reason = serializers.CharField()
    history_type = serializers.CharField()
    history_user_id = serializers.IntegerField()

class FolderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder.historical.model
        fields = ['id','history_date','history_change_reason','history_type','history_user']
    def to_representation(self,instance):
        folderResult = Folder.objects.filter(id = instance.id).first()
        return {
            'folderName':folderResult.nombre,
            'folderSlug':folderResult.slug,
            'rutaLogica': obtenerRuta(folderResult.id,[folderResult.nombre],True),
            'fechaCreacion' : instance.history_date,
            'accion':instance.history_change_reason,
            'tipo':instance.history_type,
            'history_user':instance.history_user.id
        }

class FolderBuscarSerializer(serializers.Serializer):
    buscar = serializers.CharField(allow_blank=False)
    def validate_buscar(self,value):
        return value
    def validate(self,data):
        return data
    class Meta:
        model = Folder