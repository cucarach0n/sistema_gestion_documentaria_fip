from apps.caracteristica.api.serializers.caracteristica_serializers import CaracteristicaCreateSerializer, CaracteristicaUpdateSerializer
from rest_framework.response import Response
from rest_framework import status
from apps.users.authenticacion_mixings import Authentication
from rest_framework import viewsets

class CaracteristicaViewSet(Authentication,viewsets.GenericViewSet):
    serializer_class = CaracteristicaCreateSerializer
    def get_queryset(self,pk = None):
        return self.get_serializer().Meta.model.objects.get(id = pk)
    def create(self,request):
        serializer = self.get_serializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def destroy(self,request,pk):
        caracteristica = self.get_queryset(pk)
        if caracteristica:
            caracteristica.delete()
            return Response({'mensaje':'caracteristica eliminado correctamente'},status = status.HTTP_200_OK)
        return Response({'error':'la caracteristica no existe'},status = status.HTTP_200_OK)
class CaracteristicaUpdateViewSet(Authentication, viewsets.GenericViewSet):
    serializer_class = CaracteristicaUpdateSerializer
    def get_queryset(self,pk = None):
        return self.get_serializer().Meta.model.objects.get(id = pk)
    
    def update(self,request,pk):
        caracteristica = self.get_queryset(pk)
        serializer = self.get_serializer(caracteristica,data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response({"mensaje":"actualizado correctamente"},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

