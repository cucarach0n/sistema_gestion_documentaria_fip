from datetime import datetime
import re
from apps.base.util import setHistory, validarPrivado
from rest_framework.response import Response
from rest_framework import status
from apps.folder.api.serializers.folder_in_folder_serializer import FolderInFolderUploadCreateSerializer
from apps.folder.api.serializers.general_serializer import FolderInFolder_Serializer
from apps.folder.models import Folder, FolderInFolder
from apps.folder.api.serializers.folder_serializer import FolderDetailSerializer, FolderListUploadSerializer
from apps.users.authenticacion_mixings import Authentication
from rest_framework import viewsets
from django.utils.crypto import get_random_string

def saveSubFolderUpload(self,nombreFolder,folderPadre):
    folder_data ={
            'nombre':nombreFolder,
            'scope':folderPadre.scope
    }
    folderHijo = FolderListUploadSerializer(data = folder_data,context = folderPadre)
    
    if folderHijo.is_valid():
        folderHijo.validated_data['slug'] = get_random_string(length=11)
        folderHijo.validated_data['unidadArea_id'] = self.userFull.unidadArea_id
        folderHijo.validated_data['user_id'] = self.userFull.id
        fHijo = folderHijo.save()
        folderInFolder_Serializer = FolderInFolder_Serializer(data = {
                                                    'child_folder_name':fHijo.nombre.replace(" ","_"),
                                                    'parent_folder' :folderPadre.id,
                                                    'child_folder':fHijo.id
                                                    }) 
        if folderInFolder_Serializer.is_valid():
            folderInFolder_Serializer.save()
        setHistory(fHijo,'registro nuevo subfolder',self.userFull.id)
        history = fHijo.historical.create(id=folderPadre.id,history_date = datetime.today()
                                        ,history_change_reason = "Se agrego la carpeta " + fHijo.nombre 
                                        ,history_type = "+", history_user_id = self.userFull.id )
        history.save()
        return True,fHijo
    else: 
        
        folders = FolderInFolder.objects.filter(child_folder__nombre= nombreFolder,
                                                child_folder__eliminado = False,
                                                parent_folder_id = folderPadre.id,
                                                parent_folder__eliminado = False).first()
        return False,folders.child_folder
class FolderInFolderUploadViewSet(Authentication,viewsets.GenericViewSet):
    serializer_class = FolderInFolderUploadCreateSerializer

    def get_queryset(self):
        return self.serializer_class().Meta.model.objects.all()
    
    def create(self,request):
        folderInFolder_serializer = self.serializer_class(data = request.data,context = request.data)
        if folderInFolder_serializer.is_valid():
            folderPadre = Folder.objects.filter(slug = folderInFolder_serializer.data['padreSlug'],unidadArea_id = self.userFull.unidadArea_id).first()
            if folderPadre:
                if validarPrivado(folderPadre,self.userFull.id):
                    return Response({'error':'La carpeta es privada'},status = status.HTTP_401_UNAUTHORIZED)
                pathArray = folderInFolder_serializer.validated_data['pathFolder'].split('/')
                padreNew = folderPadre
                creado = False
                for ruta in pathArray:
                    creado,padreNew =  saveSubFolderUpload(self,ruta,padreNew)

                respuesta = None
                if creado:
                    respuesta = status.HTTP_201_CREATED
                else:
                    respuesta = status.HTTP_200_OK

                folderSerializer = FolderDetailSerializer(padreNew,context = {'userId':self.userFull.id})
                return Response({'pathCreate':folderInFolder_serializer.validated_data['pathFolder'],
                                'folderCreate':folderSerializer.data},status = respuesta)
            else:
                return Response({'error':'No existe el directorio solicitado'},status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(folderInFolder_serializer.errors,status = status.HTTP_403_FORBIDDEN)