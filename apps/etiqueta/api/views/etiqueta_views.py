from apps.etiqueta.api.serializers.general_serializers import EtiquetaSerializer
from apps.etiqueta.models import Etiqueta
from apps.file.models import File
from rest_framework.response import Response
from rest_framework import status
from apps.etiqueta.api.serializers.etiqueta_serializers import EtiquetaCreateSerializer,EtiquetaBuscarSerializer, EtiquetaListSerializer
from apps.users.authenticacion_mixings import Authentication
from rest_framework import viewsets


class EtiquetaCreateViewSet(Authentication,viewsets.GenericViewSet):
    serializer_class = EtiquetaCreateSerializer

    def create(self,request):
        etiquetaSerializer = self.get_serializer(data = request.data,context = {'userId':self.userFull.id,'fileSlug':request.data['slugFile'],'idUnidadArea':self.userFull.unidadArea_id})
        if etiquetaSerializer.is_valid():
            #etiquetaSerializer.validated_data['user_id'] = self.user.id
            etiquetaCreado = etiquetaSerializer.save()
            etiquetaCreatedSerializer= EtiquetaListSerializer(etiquetaCreado)
            return Response(etiquetaCreatedSerializer.data,status = status.HTTP_200_OK)
        return Response(etiquetaSerializer.errors,status = status.HTTP_400_BAD_REQUEST)

class EtiquetaBuscarViewSet(Authentication,viewsets.GenericViewSet):
    serializer_class = EtiquetaBuscarSerializer

    def get_queryset(self,slug = None):
        return Etiqueta.objects.filter(user_id = self.userFull.id, file = File.objects.get(slug = slug,unidadArea_id = self.userFull.unidadArea_id))

    def create(self,request):
        etiquetaFindSerializer = self.get_serializer(data = request.data)
        if etiquetaFindSerializer.is_valid():
            etiquetaResultSerializer = EtiquetaSerializer(self.get_queryset(etiquetaFindSerializer.validated_data['slugFile']),many = True)        
            return Response(etiquetaResultSerializer.data,status = status.HTTP_200_OK)
        return Response(etiquetaFindSerializer.errors,status = status.HTTP_400_BAD_REQUEST)


