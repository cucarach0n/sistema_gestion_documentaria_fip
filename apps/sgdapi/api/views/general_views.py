from rest_framework import viewsets
from apps.users.authenticacion_mixings import Authentication
from rest_framework.response import Response
from rest_framework import status
from apps.sgdapi.api.serializers.general_serializers import DocumentoSerializer

class DocumentoListAPIView(Authentication,viewsets.GenericViewSet):
    serializer_class = DocumentoSerializer

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.all()

    def list(self,request):
        documentos_serializer = self.serializer_class(self.get_queryset(),many = True)
        return Response(documentos_serializer.data,status = status.HTTP_200_OK)
    
     
