from rest_framework import viewsets
from apps.users.authenticacion_mixings import Authentication
from rest_framework.response import Response
from rest_framework import status
from apps.tag.api.serializers.tag_serializer import TagCreateSerializer,TagListSerializer


class TagListAPIView(viewsets.GenericViewSet):
    serializer_class = TagListSerializer

    def get_queryset(self,pk = None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.all()
        else:
            return self.get_serializer().Meta.model.objects.filter(id = pk)
    def list(self,request):
        tag_serializer = self.serializer_class(self.get_queryset(),many = True)
        return Response(tag_serializer.data,status = status.HTTP_200_OK)
    def retrieve(self,request,pk =None):
        tag_serializer = self.serializer_class(self.get_queryset(pk).first())
        if tag_serializer:
            return Response(tag_serializer.data,status = status.HTTP_200_OK)
        return Response({'error':'No se encontro el tag'},status = status.HTTP_400_BAD_REQUEST)

class TagAPIView(viewsets.GenericViewSet):
    serializer_class = TagCreateSerializer

    def get_queryset(self,pk = None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.all()
        else:
            return self.get_serializer().Meta.model.objects.filter(id = pk)

    def create(self,request):
        tag_serializer = self.serializer_class(data = request.data)
        if tag_serializer.is_valid():
            tag_serializer.save()
            return Response({'mensaje':'Se registros correctamente el tag'},status = status.HTTP_200_OK)
        else:
            return Response(tag_serializer.errors,status = status.HTTP_400_BAD_REQUEST)
    
    def update(self,request,pk=None):
        tag = self.get_queryset(pk).first()
        if tag:
            tag_serializer = self.serializer_class(tag , data = request.data)
            if tag_serializer.is_valid():
                tag_serializer.save()
                return Response({'mensaje':'Se actualizo correctamente el tag'},status = status.HTTP_200_OK)
            return Response(tag_serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        return Response({'error':'No existe el tag'},status = status.HTTP_400_BAD_REQUEST)
            
    
     
