from apps.caracteristica.api.serializers.caracteristicaFile_serializers import CaracteristicaFileCreateSerializer,CaracteristicaFileDeleteSerializer
from rest_framework.response import Response
from rest_framework import status
from apps.users.authenticacion_mixings import Authentication
from rest_framework import viewsets

class CaracteristicaFileViewSet(Authentication,viewsets.GenericViewSet):
    serializer_class = CaracteristicaFileCreateSerializer
    def create(self,request):
        serializer = self.get_serializer(data=request.data,context = request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response({'mensaje':'creado satisfactoriamente'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk=None):
        serializer = CaracteristicaFileDeleteSerializer(data=request.data,context = request.data)
        if(serializer.is_valid()):
            serializer.delete()
            return Response({'mensaje':'eliminado satisfactoriamente'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)