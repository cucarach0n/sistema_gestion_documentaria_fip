from dataclasses import dataclass
from apps.base.util import validarCompartido
from apps.folder.api.serializers.folder_serializer import FolderDirecotorioListSerializer
from apps.folder.models import Folder
from apps.share.api.serializers.folderShare_serializers import FolderShareCreateSerializer, FolderShareValidateCreateSerializer
from apps.share.models import FolderShare
from rest_framework.response import Response
from rest_framework import status
from apps.users.authenticacion_mixings import Authentication
from rest_framework import viewsets

class FolderShareViewSet(Authentication,viewsets.GenericViewSet):
    serializer_class = FolderShareCreateSerializer

    def get_queryset(self,pk = None):
        if pk is None:
            return Folder.objects.filter(foldershare__estado = True,foldershare__userTo_id = self.userFull.id)
        else:
            return Folder.objects.filter(slug = pk)
    def create(self,request):
        folderShareSerializer = self.get_serializer(data = request.data,context = {'userId':self.userFull.id,'unidadId':self.userFull.unidadArea_id})
        if folderShareSerializer.is_valid():
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
        folderAllShareSerialiser = FolderDirecotorioListSerializer(self.get_queryset(),many = True,context = {'userId':self.userFull.id,'userStaff': 5})        
        return Response(folderAllShareSerialiser.data,status = status.HTTP_200_OK)
    
    def retrieve(self,request,pk):
        
        folderResult = self.get_queryset(pk)
        if folderResult:
            if not validarCompartido(folderResult.first().slug,False,self.userFull.id):
                return Response({'error':'La carpeta solicitada no esta disponible'},status = status.HTTP_401_UNAUTHORIZED)
            folderSerializer = FolderDirecotorioListSerializer(folderResult,many = True,context = {'userId':self.userFull.id,'userStaff': 5})
            return Response(folderSerializer.data,status = status.HTTP_200_OK)
        return Response({'error':'La carpeta no existe'},status = status.HTTP_400_BAD_REQUEST)
            