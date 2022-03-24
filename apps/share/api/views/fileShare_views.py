from apps.base.util import validarCompartido
from apps.file.api.serializers.file_serializers import FileDetalleSerializer
from apps.file.models import File
from apps.folder.models import Folder
from apps.share.api.serializers.fileShare_serializers import FileShareCreateSerializer, FileShareValidateCreateSerializer
from rest_framework.response import Response
from rest_framework import status
from apps.users.authenticacion_mixings import Authentication
from rest_framework import viewsets

class FileShareViewSet(Authentication,viewsets.GenericViewSet):
    serializer_class = FileShareCreateSerializer

    def get_queryset(self,pk = None):
        if pk is None:
            return File.objects.filter(fileshare__estado = True,fileshare__userTo_id = self.userFull.id)
        else:
            return File.objects.filter(fileshare__estado = True,fileshare__file__slug = pk,fileshare__userTo__id = self.userFull.id)
    def create(self,request):
        fileShareSerializer = self.get_serializer(data = request.data,context = {'userId':self.userFull.id,'unidadId':self.userFull.unidadArea_id})
        if fileShareSerializer.is_valid():
            fileShareValidateSerializer = FileShareValidateCreateSerializer(data = {
                'file':fileShareSerializer.validated_data['slugFile'],
                'userTo':fileShareSerializer.validated_data['correoTo'],
                'userFrom':self.userFull.id
            })
            if fileShareValidateSerializer.is_valid():

                '''folderCreate = FolderShare()
                folderCreate.folder_id = folderShareSerializer.validated_data['slugFolder']
                folderCreate.userFrom_id = self.userFull.id
                folderCreate.userTo_id = folderShareSerializer.validated_data['correoTo']
                folderCreate.save()'''
                fileShareValidateSerializer.save()
                return Response({'mensaje':'Se compartio exitosamente el file con el usuario'},status = status.HTTP_200_OK)
            return Response(fileShareValidateSerializer.errors,status = status.HTTP_400_BAD_REQUEST)
        return Response(fileShareSerializer.errors,status = status.HTTP_400_BAD_REQUEST)
    '''def list(self,request):
        fileAllShareSerialiser = FileDetalleSerializer(self.get_queryset(),many = True)        
        return Response(fileAllShareSerialiser.data,status = status.HTTP_200_OK)'''
    
    def retrieve(self,request,pk):
        
        fileResult = self.get_queryset(pk)
        if fileResult:
            fileSerializer = FileDetalleSerializer(fileResult,many = True)      
            return Response(fileSerializer.data,status = status.HTTP_200_OK)
        return Response({'error':'El file no existe o no tiene acceso'},status = status.HTTP_400_BAD_REQUEST)
            