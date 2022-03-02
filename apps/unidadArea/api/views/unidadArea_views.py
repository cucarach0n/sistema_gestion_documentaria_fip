from apps.folder.api.serializers.folder_serializer import FolderSerializer
from rest_framework import viewsets
from apps.users.authenticacion_mixings import Authentication
from rest_framework.response import Response
from rest_framework import status
from apps.unidadArea.api.serializers.general_serializers import UnidadArea_Serializer
from apps.unidadArea.api.serializers.unidadArea_serializers import UnidadAreaCreate_Serializer,UnidadAreaDeleteSerializer
from django.utils.crypto import get_random_string  

class unidadAreaCreateAPIView(viewsets.GenericViewSet):
    serializer_class = UnidadAreaCreate_Serializer
    def create(self,request):
        unidadArea_serializer = self.serializer_class(data = request.data)
        if unidadArea_serializer.is_valid():
            
            unidadArea = unidadArea_serializer.save()

            folder_serializer = FolderSerializer(data = {
                    'nombre': unidadArea.nombreUnidad,
                    'unidadArea':unidadArea.id
                })
            if folder_serializer.is_valid():
                folder_serializer.validated_data['slug'] = get_random_string(length=11) 
                folder_serializer.save()
                return Response({
                    'idUnidad': unidadArea.id,
                    'nombreUnidad' : unidadArea.nombreUnidad
                },status = status.HTTP_200_OK)
            else:
                return Response(folder_serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        return Response(unidadArea_serializer.errors,status = status.HTTP_400_BAD_REQUEST)


class unidadAreaListAPIView(viewsets.GenericViewSet):
    serializer_class = UnidadArea_Serializer

    def get_queryset(self,pk = None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.all()
        return self.get_serializer().Meta.model.objects.filter(id = pk)

    def list(self,request):
        unidadArea_serializer = self.serializer_class(self.get_queryset(),many = True)
        return Response(unidadArea_serializer.data,status = status.HTTP_200_OK)
    def retrieve(self,reques,pk = None):
        unidadArea_serializer = self.serializer_class(self.get_queryset(pk).first())
        if unidadArea_serializer:
            return Response(unidadArea_serializer.data,status = status.HTTP_200_OK)
        return Response({'error':'No existe la unidad'},status = status.HTTP_400_BAD_REQUEST)

class unidadAreaBuscarAPIView(viewsets.GenericViewSet):

    serializer_class = UnidadArea_Serializer
    def get_queryset(self,pk = None):
        return self.get_serializer().Meta.model.objects.filter(nombreUnidad__icontains = pk)
    
    def create(self,request):
        if request.POST.get('nombreUnidad') is not None:
            unidadAreaBusqueda_serializer = self.get_serializer(request.data)
            if unidadAreaBusqueda_serializer:
                unidadArea_serializer = self.serializer_class(self.get_queryset(unidadAreaBusqueda_serializer.data['nombreUnidad']),many = True)
                return Response(unidadArea_serializer.data,status = status.HTTP_200_OK)
        else:
            return Response({'error':'Se produjo un error en la busqueda'},status = status.HTTP_400_BAD_REQUEST)
       
class unidadAreaDeleteAPIView(Authentication,viewsets.GenericViewSet):
    serializer_class = UnidadAreaDeleteSerializer
    def get_queryset(self,pk = None):
        return self.get_serializer().Meta.model.objects.filter(id = pk).first()
    
    def destroy(self,request,pk = None):
        unidadAreaSerializer = self.get_serializer(data = request.data)
        if unidadAreaSerializer.is_valid():
            if self.userFull.is_superuser:
                unidadAreaDeleteResult = self.get_queryset(pk)
                unidadAreaDeleteResult.delete()
                return Response({'Mensaje':'Unidad Area eliminado correctamente'},status = status.HTTP_200_OK)
            else:
                return Response({'Error':'No permitido'},status = status.HTTP_400_BAD_REQUEST)  
        else:
            return Response(unidadAreaSerializer.errors,status = status.HTTP_400_BAD_REQUEST) 
        


    
     
