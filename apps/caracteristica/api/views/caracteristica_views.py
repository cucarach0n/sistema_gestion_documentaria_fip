from apps.caracteristica.api.serializers.caracteristica_serializers import CaracteristicaCreateSerializer
from rest_framework.response import Response
from rest_framework import status
from apps.users.authenticacion_mixings import Authentication
from rest_framework import viewsets

class CaracteristicaViewSet(Authentication,viewsets.GenericViewSet):
    serializer_class = CaracteristicaCreateSerializer
    def create(self,request):
        serializer = self.get_serializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

