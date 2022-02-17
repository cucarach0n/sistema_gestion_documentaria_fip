from rest_framework import viewsets
from apps.users.authenticacion_mixings import Authentication
from rest_framework.response import Response
from rest_framework import status
from apps.unidadArea.api.serializers.general_serializers import UnidadArea_Serializer
from apps.unidadArea.api.serializers.unidadArea_serializers import UnidadAreaCreate_Serializer


class unidadAreaCreateAPIView(viewsets.GenericViewSet):
    serializer_class = UnidadAreaCreate_Serializer
    def create(self,request):
        unidadArea_serializer = self.serializer_class(data = request.data)
        if unidadArea_serializer.is_valid():
            unidadArea_serializer.save()
            return Response({'mensaje':'Unidad creada exitosamente'},status = status.HTTP_200_OK)
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
       
        
        


    
     
