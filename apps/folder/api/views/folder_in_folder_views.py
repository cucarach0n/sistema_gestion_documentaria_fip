from datetime import datetime
from apps.base.util import setHistory
from rest_framework.response import Response
from rest_framework import status
from apps.folder.api.serializers.folder_in_folder_serializer import FolderInFolderValidateCreateSerializer
from apps.folder.api.serializers.general_serializer import FolderInFolder_Serializer
from apps.folder.models import Folder, FolderInFolder
from apps.folder.api.serializers.folder_serializer import FolderDetailSerializer, FolderListSerializer
from apps.users.authenticacion_mixings import Authentication
from django.conf import settings
from rest_framework import viewsets
from django.utils.crypto import get_random_string

def obtenerRutaAbsoluta(padreId,ruta):
        #si el padre es null
        #print('obteniendo ruta')
        folderinfolder = FolderInFolder.objects.filter(child_folder_id = padreId).select_related('child_folder').first()
        if folderinfolder:
            ruta.append(folderinfolder.parent_folder.slug) 
            obtenerRutaAbsoluta(folderinfolder.parent_folder_id,ruta )
        return '/'.join(ruta[::-1])
class FolderInFolderViewSet(Authentication,viewsets.GenericViewSet):
    serializer_class = FolderInFolderValidateCreateSerializer

    def get_queryset(self):
        return self.serializer_class().Meta.model.objects.all()
    
    def list(self,request):
        folders = self.serializer_class(self.get_queryset(),many = True)
        return Response(folders.data,status = status.HTTP_200_OK)
    
    
    
    def create(self,request):
        folderInFolder_serializer = self.serializer_class(data = request.data,context = request.data)
        if folderInFolder_serializer.is_valid():
            folderPadre = Folder.objects.filter(slug = folderInFolder_serializer.data['padreSlug'],unidadArea_id = self.userFull.unidadArea_id).first()
            if folderPadre:
                folder_data ={
                        'nombre':folderInFolder_serializer.validated_data['child_folder_name']
                }
                folderHijo = FolderListSerializer(data = folder_data,context = folderPadre)
                
                if folderHijo.is_valid():
                    folderHijo.validated_data['slug'] = get_random_string(length=11)
                    folderHijo.validated_data['unidadArea_id'] = self.userFull.unidadArea_id
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
                    folderDetailSerializer = FolderDetailSerializer(fHijo)
                    #set history subfolder
                    setHistory(fHijo,'registro nuevo subfolder',self.userFull.id)
                    #add history folderPadre
                    history = fHijo.historical.create(id=folderPadre.id,history_date = datetime.today()
                                                    ,history_change_reason = "Se agrego la carpeta " + fHijo.nombre.replace(" ","_") 
                                                    ,history_type = "+", history_user_id = self.userFull.id )
                    history.save()
                    return Response(folderDetailSerializer.data,status = status.HTTP_200_OK)

                    #return Response({"slug":fHijo.slug,'name':fHijo.nombre},status = status.HTTP_200_OK)
                else:
                    return Response(folderHijo.errors,status = status.HTTP_400_BAD_REQUEST)     
            else:
                return Response({'error':'No existe el directorio solicitado'},status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(folderInFolder_serializer.errors,status = status.HTTP_403_FORBIDDEN)
