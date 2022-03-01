import re
from rest_framework.response import Response
from rest_framework import status
from apps.etiqueta.api.serializers.etiqueta_serializers import EtiquetaCreateSerializer
from apps.users.authenticacion_mixings import Authentication
import os
from django.conf import settings
from rest_framework import viewsets


class EtiquetaViewSet(Authentication,viewsets.GenericViewSet):
    serializer_class = EtiquetaCreateSerializer

    def create(self,request):
        etiquetaSerializer = self.get_serializer(data = request.data,context = {'userId':self.userFull.id,'fileSlug':request.data['slugFile']})
        if etiquetaSerializer.is_valid():
            #etiquetaSerializer.validated_data['user_id'] = self.user.id
            etiquetaSerializer.save()
            return Response({'mensaje':'Se registro la etiqueta correctamente'},status = status.HTTP_200_OK)
        return Response(etiquetaSerializer.errors,status = status.HTTP_400_BAD_REQUEST)