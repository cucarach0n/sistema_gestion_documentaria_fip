from apps.caracteristica.api.serializers.tipoCaracteristica_serializers import TipoCaracteristicaCreateSerializer, TipoCaracteristicaListSerializer
from apps.caracteristica.models import TipoCaracteristica
from rest_framework.response import Response
from rest_framework import status
from apps.users.authenticacion_mixings import Authentication
from rest_framework import viewsets

class tipoCaracteristicaViewSet(Authentication,viewsets.GenericViewSet):
    serializer_class = TipoCaracteristicaListSerializer
    def get_queryset(self):
        return TipoCaracteristica.objects.all()
    def create(self,request):
        serializer = TipoCaracteristicaCreateSerializer(data=request.data)
        if(serializer.is_valid()):
            tipoCaracteristicaCreate = serializer.save()
            return Response({'id':tipoCaracteristicaCreate.id,
                            'nombreTipo':tipoCaracteristicaCreate.nombreTipo},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def list(self,request):
        tipoCaracteristica = self.get_queryset()
        return Response(self.serializer_class(tipoCaracteristica,many=True).data,status=status.HTTP_200_OK)