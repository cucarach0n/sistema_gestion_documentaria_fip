from apps.base.util import setHistory
from apps.folder.api.serializers.folder_serializer import FolderSerializer
from apps.folder.models import Folder
from rest_framework import viewsets
from apps.users.authenticacion_mixings import Authentication
from rest_framework.response import Response
from rest_framework import status
from apps.unidadArea.api.serializers.general_serializers import UnidadArea_Serializer
from apps.unidadArea.api.serializers.unidadArea_serializers import UnidadAreaCreate_Serializer,UnidadAreaDeleteSerializer, UnidadAreaUpdate_Serializer
from django.utils.crypto import get_random_string  

class unidadAreaCreateAPIView(Authentication,viewsets.GenericViewSet):
    serializer_class = UnidadAreaCreate_Serializer
    def create(self,request):
        unidadArea_serializer = self.serializer_class(data = request.data)
        if self.userFull.is_superuser:
            if unidadArea_serializer.is_valid():
                
                unidadArea = unidadArea_serializer.save()

                folder_serializer = FolderSerializer(data = {
                        'nombre': unidadArea.nombreUnidad,
                        'unidadArea':unidadArea.id
                    })
                if folder_serializer.is_valid():
                    folder_serializer.validated_data['slug'] = get_random_string(length=11) 
                    folder_serializer.validated_data['user_id'] = self.userFull.id 
                    folderSave = folder_serializer.save()
                    #set history unidadArea
                    setHistory(folderSave,'registro nuevo folder master',self.userFull.id)
                    return Response({
                        'idUnidad': unidadArea.id,
                        'nombreUnidad' : unidadArea.nombreUnidad
                    },status = status.HTTP_200_OK)
                else:
                    return Response(folder_serializer.errors,status = status.HTTP_400_BAD_REQUEST)
            return Response(unidadArea_serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        return Response({'Error':'No permitido'},status = status.HTTP_403_FORBIDDEN)  


class unidadAreaListAPIView(Authentication,viewsets.GenericViewSet):
    serializer_class = UnidadArea_Serializer

    def get_queryset(self,pk = None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.all()
        return self.get_serializer().Meta.model.objects.filter(id = pk)

    def list(self,request):
        if self.userFull.is_superuser:
            unidadArea_serializer = self.serializer_class(self.get_queryset(),many = True)
            return Response(unidadArea_serializer.data,status = status.HTTP_200_OK)
        return Response({'Error':'No permitido'},status = status.HTTP_403_FORBIDDEN)  
    def retrieve(self,reques,pk = None):
        if self.userFull.is_superuser:
            unidadArea_serializer = self.serializer_class(self.get_queryset(pk).first())
            if unidadArea_serializer:
                return Response(unidadArea_serializer.data,status = status.HTTP_200_OK)
            return Response({'error':'No existe la unidad'},status = status.HTTP_400_BAD_REQUEST)
        return Response({'Error':'No permitido'},status = status.HTTP_403_FORBIDDEN)  
class unidadAreaUpdatePIView(Authentication,viewsets.GenericViewSet):
    serializer_class = UnidadAreaUpdate_Serializer

    def get_queryset(self,pk = None):
        return self.get_serializer().Meta.model.objects.get(id = pk)
    def update(self,reques,pk = None):
        if self.userFull.is_superuser:
            unidadArea_serializer = self.serializer_class(self.get_queryset(pk),data = reques.data)
            if unidadArea_serializer.is_valid():
                folderGestion = Folder.objects.filter(carpeta_hija__isnull =True,unidadArea_id = pk).first()
                folderGestion.nombre = unidadArea_serializer.validated_data['nombreUnidad']
                folderGestion.save()
                unidadArea_serializer.save()
                return Response({'mensaje':'actualizado correctamente'},status = status.HTTP_200_OK)
            return Response(unidadArea_serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        return Response({'Error':'No permitido'},status = status.HTTP_403_FORBIDDEN)
        
class unidadAreaBuscarAPIView(Authentication,viewsets.GenericViewSet):

    serializer_class = UnidadArea_Serializer
    def get_queryset(self,pk = None):
        return self.get_serializer().Meta.model.objects.filter(nombreUnidad__icontains = pk)
    
    def create(self,request):
        if self.userFull.is_superuser:
            if request.POST.get('nombreUnidad') is not None:
                unidadAreaBusqueda_serializer = self.get_serializer(request.data)
                if unidadAreaBusqueda_serializer:
                    unidadArea_serializer = self.serializer_class(self.get_queryset(unidadAreaBusqueda_serializer.data['nombreUnidad']),many = True)
                    return Response(unidadArea_serializer.data,status = status.HTTP_200_OK)
            else:
                return Response({'error':'Se produjo un error en la busqueda'},status = status.HTTP_400_BAD_REQUEST)
        return Response({'Error':'No permitido'},status = status.HTTP_403_FORBIDDEN)  
class unidadAreaDeleteAPIView(Authentication,viewsets.GenericViewSet):
    serializer_class = UnidadAreaDeleteSerializer
    def get_queryset(self,pk = None):
        return self.get_serializer().Meta.model.objects.filter(id = pk).first()
    
    def destroy(self,request,pk = None):        
        if self.userFull.is_superuser:
            unidadAreaSerializer = self.get_serializer(data = request.data)
            if unidadAreaSerializer.is_valid():
                unidadAreaDeleteResult = self.get_queryset(pk)
                unidadAreaDeleteResult.delete()
                
                return Response({'Mensaje':'Unidad Area eliminado correctamente'},status = status.HTTP_200_OK) 
            else:
                return Response(unidadAreaSerializer.errors,status = status.HTTP_400_BAD_REQUEST) 
        return Response({'Error':'No permitido'},status = status.HTTP_403_FORBIDDEN)  


    
     
