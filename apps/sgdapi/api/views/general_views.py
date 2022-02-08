from multiprocessing import context
from rest_framework import viewsets

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from apps.sgdapi.api.serializers.general_serializers import DocumentoSerializer

class DocumentoListAPIView(viewsets.ModelViewSet):
    serializer_class = DocumentoSerializer
#    def get_queryset(self):
#        return self.get_serializer().Meta.model.objects.all()

