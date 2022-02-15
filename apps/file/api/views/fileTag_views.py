from rest_framework import viewsets
from apps.users.authenticacion_mixings import Authentication
from rest_framework.response import Response
from rest_framework import status
from apps.file.api.serializers.filaTag_serializer import FileTagSerializer,FileTagCreateSerializer,FileTagDeleteSerializer
from apps.file.api.serializers.general_serializers import FileTag_Serializer


class FileTagDeleteAPIView(viewsets.GenericViewSet):
    serializer_class = FileTagDeleteSerializer

    def create(self,request):
        fileTag_serializer = self.serializer_class(data = request.data,context =  request.data)
        if fileTag_serializer.is_valid():
            fileTag_serializer.delete()
            return Response({'mensaje':'se elimino correctamente'},status = status.HTTP_200_OK)
        return Response(fileTag_serializer.errors,status = status.HTTP_400_BAD_REQUEST)

class FileTagAPIView(viewsets.GenericViewSet):
    serializer_class = FileTagCreateSerializer

    '''def get_queryset(self):
        return self.get_serializer().Meta.model.objects.all()'''

    def create(self,request):
        fileTag_serializer = self.serializer_class(data = request.data,context =  request.data)
        if fileTag_serializer.is_valid():
            fileTag_serializer.save()
            return Response({'mensaje':'se registro exitosamente'},status = status.HTTP_200_OK)
        return Response(fileTag_serializer.errors,status = status.HTTP_400_BAD_REQUEST)
    
     
