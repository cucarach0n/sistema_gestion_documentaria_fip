from apps.base.util import shareFile_email
from apps.file.api.serializers.fileEmail_serializer import FileEmailShareSerializer
from rest_framework import viewsets
from apps.users.authenticacion_mixings import Authentication
from rest_framework.response import Response
from rest_framework import status

class FileShareEmailAPIView(Authentication,viewsets.GenericViewSet):
    serializer_class = FileEmailShareSerializer
    def create(self,request):
        file_serializer = self.serializer_class(data = request.data)
        if file_serializer.is_valid():
            #enviar email

            shareFile_email({'email':file_serializer.validated_data['emailDestino'],
                            'usuario':self.userFull,
                            'asunto':file_serializer.validated_data['asunto'],
                            'mensaje':file_serializer.validated_data['mensaje']},file_serializer.validated_data['fileSlug'])
            return Response({'mensaje':'se compartio correctamente exitosamente'},status = status.HTTP_200_OK)
        return Response(file_serializer.errors,status = status.HTTP_400_BAD_REQUEST)
    
     
