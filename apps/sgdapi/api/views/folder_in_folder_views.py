from multiprocessing import context
from os import stat
import re
from rest_framework.response import Response
from rest_framework import status
from apps.sgdapi.api.serializers.folder_in_folder_serializer import FolderInFolderValidateCreateSerializer
from apps.sgdapi.api.serializers.general_serializers import FolderInFolder_Serializer
from apps.sgdapi.models import Folder, FolderInFolder
from apps.sgdapi.api.serializers.folder_serializer import FolderListSerializer
from apps.users.authenticacion_mixings import Authentication
from django.conf import settings
from rest_framework import viewsets
from django.utils.crypto import get_random_string

def obtenerRutaAbsoluta(padreId,ruta):
        #si el padre es null
        print('obteniendo ruta')
        folderinfolder = FolderInFolder.objects.filter(child_folder_id = padreId).select_related('child_folder').first()
        if folderinfolder:
            ruta.append(folderinfolder.parent_folder.slug) 
            obtenerRutaAbsoluta(folderinfolder.parent_folder_id,ruta )
        return '/'.join(ruta[::-1])
class FolderInFolderViewSet(viewsets.GenericViewSet):
    serializer_class = FolderInFolderValidateCreateSerializer

    def get_queryset(self):
        return self.serializer_class().Meta.model.objects.all()
    
    def list(self,request):
        folders = self.serializer_class(self.get_queryset(),many = True)
        return Response(folders.data,status = status.HTTP_200_OK)
    
    
    
    def create(self,request):
        folderInFolder_serializer = self.serializer_class(data = request.data,context = request.data)
        if folderInFolder_serializer.is_valid():
            folderPadre = Folder.objects.filter(slug = folderInFolder_serializer.data['padreSlug']).first()
            if folderPadre:
                folder_data ={
                        'nombre':folderInFolder_serializer.validated_data['child_folder_name']
                }
                folderHijo = FolderListSerializer(data = folder_data,context = folderPadre)
                
                if folderHijo.is_valid():
                    folderHijo.validated_data['slug'] = get_random_string(length=6)
                    fHijo = folderHijo.save()
                    folderInFolder_Serializer = FolderInFolder_Serializer(data = {
                                                                'child_folder_name':fHijo.nombre.replace(" ","_"),
                                                                'parent_folder' :folderPadre.id,
                                                                'child_folder':fHijo.id
                                                                }) 
                    if folderInFolder_Serializer.is_valid():
                        '''
                        ruta =[]
                        ruta.append(folderPadre.slug)
                        ruta = obtenerRutaAbsoluta(folderPadre.id,ruta)
                        print(ruta +"/"+ fHijo.slug)
                        try:
                            os.makedirs(settings.MEDIA_ROOT + "files/"+ruta +"/"+ fHijo.slug, exist_ok=True)
                        except:
                            print('Error al crear el Subdirectorio')
                            Response({'error':"Hubo un error al crear el Subdirectorio"},status = status.HTTP_400_BAD_REQUEST)    
                        '''          
                        folderInFolder_Serializer.save()

                    return Response({'Mensaje':"Se registro correctamente el Subdirectorio"},status = status.HTTP_200_OK)
                else:
                    return Response(folderHijo.errors,status = status.HTTP_400_BAD_REQUEST)     
            else:
                return Response({'error':'No existe el directorio solicitado'},status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(folderInFolder_serializer.errors,status = status.HTTP_403_FORBIDDEN)

        