# -*- coding: utf-8 -*-
import os
from apps.file.models import FileInFolder
from apps.folder.models import Folder
from rest_framework.response import Response
from rest_framework import status
from apps.file.api.serializers.file_serializers import (
    FileDetalleSerializer
    )
from apps.users.authenticacion_mixings import Authentication
from django.conf import settings
from rest_framework import viewsets

class FileDeletePublicAPIView(Authentication,viewsets.GenericViewSet):
    serializer_class = FileDetalleSerializer
    def get_queryset(self,pk):
        return self.get_serializer().Meta.model.objects.filter(slug = pk,scope = True,unidadArea_id = self.userFull.unidadArea_id)    
    def retrieve(self,request,pk):
        fileResult = self.get_queryset(pk).first()
        if fileResult:
            #fileSerializer = self.get_serializer(fileResult)
            if fileResult.eliminado:
                rutaFile = settings.MEDIA_ROOT+'files/'
                os.remove(os.path.join(rutaFile+fileResult.documento_file.name))
                fileResult.delete()
                return Response({'mensaje':'File destruido correctamente'}, status = status.HTTP_200_OK)
            folderMasterPublic = Folder.objects.get(user__is_superuser = True,
                                                    carpeta_hija__isnull =True,
                                                    unidadArea_id = self.userFull.unidadArea_id,eliminado = False,scope = True)
            fileResult.eliminado = True
            fileResult.save()
            FileInFolder.objects.filter(file_id = fileResult.id).update(parent_folder_id = folderMasterPublic.id)
            return Response({'mensaje':'File eliminado correctamente'}, status = status.HTTP_200_OK)
        return Response({'error':'No existe el file'},status = status.HTTP_401_UNAUTHORIZED)
class FileRestaurarPublicAPIView(Authentication,viewsets.GenericViewSet):
    serializer_class = FileDetalleSerializer
    def get_queryset(self,pk):
        return self.get_serializer().Meta.model.objects.filter(slug = pk,scope = True,unidadArea_id = self.userFull.unidadArea_id,eliminado = True)    
    def retrieve(self,request,pk):
        fileResult = self.get_queryset(pk).first()
        if fileResult:
            folderMasterPublic = Folder.objects.get(user__is_superuser = True,
                                                    carpeta_hija__isnull =True,
                                                    unidadArea_id = self.userFull.unidadArea_id,eliminado = False,scope = True)
            fileResult.eliminado = False
            fileResult.save()
            FileInFolder.objects.filter(file_id = fileResult.id).update(parent_folder_id = folderMasterPublic.id)
            return Response({'mensaje':'File restaurado a la carpeta ' + folderMasterPublic.nombre}, status = status.HTTP_200_OK)
        return Response({'error':'No existe el file'},status = status.HTTP_401_UNAUTHORIZED)