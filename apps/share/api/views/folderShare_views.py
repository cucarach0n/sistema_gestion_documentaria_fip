from apps.base.util import clonarCarpetaCompartida, validarCompartido
from apps.file.api.serializers.file_serializers import FileDetalleShareSerializer
from apps.folder.api.serializers.folder_serializer import FolderDirecotorioListSerializer, FolderDirecotorioListShareSerializer
from apps.folder.models import Folder
from apps.share.api.serializers.fileShare_serializers import FileShareCreateSerializer
from apps.share.api.serializers.folderShare_serializers import FolderShareClonarSerializer, FolderShareCreateSerializer, FolderShareValidateCreateSerializer
from apps.folder.api.serializers.treefolder_serializer import TreeFolderSerializer
from apps.share.models import FolderShare
from apps.file.models import File
from rest_framework.response import Response
from rest_framework import status
from apps.users.authenticacion_mixings import Authentication
from rest_framework import viewsets

class FolderShareCloneViewSet(Authentication,viewsets.GenericViewSet):
    serializer_class = FolderShareClonarSerializer
    def get_queryset(self,pk):
        return self.get_serializer().Meta.model.objects.get(slug = pk,eliminado=False)
    def retrieve(self,request,pk):
        folderResult = self.get_queryset(pk)
        if folderResult:
            if not validarCompartido(folderResult.slug,False,self.userFull.id):
                return Response({'error':'La carpeta solicitada no esta disponible'},status = status.HTTP_401_UNAUTHORIZED)
            if Folder.objects.filter(user_id = self.userFull.id,scope=False,nombre = folderResult.nombre):
                return Response({'error':'La carpeta ya existe'},status = status.HTTP_400_BAD_REQUEST)
            folderMaster = Folder.objects.filter(scope = False,
                                                unidadArea_id = self.userFull.unidadArea_id,
                                                user_id =self.userFull.id,
                                                carpeta_hija__isnull =True).first()
            clonarCarpetaCompartida(folderResult.slug,self.userFull,folderMaster.id)
            return Response({'mensaje':'carpeta clonada'},status = status.HTTP_200_OK)
        return Response({"error":"la carpeta no existe"},status = status.HTTP_400_BAD_REQUEST)    
class FolderShareViewSet(Authentication,viewsets.GenericViewSet):
    serializer_class = FolderShareCreateSerializer

    def get_queryset(self,pk = None):
        if pk is None:
            return Folder.objects.filter(eliminado=False,foldershare__estado = True,foldershare__userTo_id = self.userFull.id)
        else:
            return Folder.objects.filter(slug = pk,eliminado=False,)
    def create(self,request):
        
        folderShareSerializer = self.get_serializer(data = request.data,context = {'userId':self.userFull.id,'unidadId':self.userFull.unidadArea_id})
        if folderShareSerializer.is_valid():
            #if Folder.objects.filter(carpeta_hija__isnull =True,unidadArea_id = self.userFull.unidadArea_id,slug = folderShareSerializer.validated_data['slugFolder']):
            #    return Response({'mensaje':'Esta carpeta no se puede compartir'},status = status.HTTP_401_UNAUTHORIZED)
            folderShareValidateSerializer = FolderShareValidateCreateSerializer(data = {
                'folder':folderShareSerializer.validated_data['slugFolder'],
                'userTo':folderShareSerializer.validated_data['correoTo'],
                'userFrom':self.userFull.id
            })
            if folderShareValidateSerializer.is_valid():

                '''folderCreate = FolderShare()
                folderCreate.folder_id = folderShareSerializer.validated_data['slugFolder']
                folderCreate.userFrom_id = self.userFull.id
                folderCreate.userTo_id = folderShareSerializer.validated_data['correoTo']
                folderCreate.save()'''
                folderShareValidateSerializer.save()
                return Response({'mensaje':'Se compartio exitosamente el folder con el usuario'},status = status.HTTP_200_OK)
            return Response(folderShareValidateSerializer.errors,status = status.HTTP_400_BAD_REQUEST)
        return Response(folderShareSerializer.errors,status = status.HTTP_400_BAD_REQUEST)
    def list(self,request):
        folderAllShareSerialiser = FolderDirecotorioListShareSerializer(self.get_queryset(),many = True,context = {'userId':self.userFull.id,'userStaff': 5})
        files = FileDetalleShareSerializer(File.objects.filter(fileshare__estado = True,fileshare__userTo_id = self.userFull.id),many = True)   
        arbol = TreeFolderSerializer(self.get_queryset(),many = True)
        #return Response(folderAllShareSerialiser.data,status = status.HTTP_200_OK)
        return Response({
            'nombre':'Carpeta compartida',
            'subDirectorios': folderAllShareSerialiser.data,
            'files':files.data,
            'treefolders':arbol.data           
        },status = status.HTTP_200_OK)
    def retrieve(self,request,pk):
        
        folderResult = self.get_queryset(pk)
        if folderResult:
            if not validarCompartido(folderResult.first().slug,False,self.userFull.id):
                return Response({'error':'La carpeta solicitada no esta disponible'},status = status.HTTP_401_UNAUTHORIZED)
            folderSerializer = FolderDirecotorioListShareSerializer(folderResult,many = True,context = {'userId':self.userFull.id,'userStaff': 5})
            return Response(folderSerializer.data,status = status.HTTP_200_OK)
        return Response({'error':'La carpeta no existe'},status = status.HTTP_400_BAD_REQUEST)
            