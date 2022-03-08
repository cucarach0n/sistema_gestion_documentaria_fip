from datetime import datetime
from apps.base.util import setHistory
from rest_framework import viewsets
from apps.users.authenticacion_mixings import Authentication
from rest_framework.response import Response
from rest_framework import status
from apps.tag.api.serializers.tag_serializer import TagCreateSerializer,TagListSerializer
from django.db.models import Q
from django.core.paginator import Paginator

class TagBuscarAPIView(viewsets.GenericViewSet):

    serializer_class = TagListSerializer
    def get_queryset(self,pk = None):
        return self.get_serializer().Meta.model.objects.filter(tagName__icontains = pk)
    
    def create(self,request):
        print(request.POST.get('tagName'))
        if request.POST.get('tagName') is not None:
            tagBusqueda_serializer = self.get_serializer(request.data)
            if tagBusqueda_serializer:
                tagArea_serializer = self.serializer_class(self.get_queryset(tagBusqueda_serializer.data['tagName']),many = True)
                return Response(tagArea_serializer.data,status = status.HTTP_200_OK)
        else:
            return Response({'error':'Se produjo un error en la busqueda'},status = status.HTTP_400_BAD_REQUEST)


class TagListAPIView(viewsets.GenericViewSet):
    serializer_class = TagListSerializer

    def get_queryset(self,pk = None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.all()
        else:
            return self.get_serializer().Meta.model.objects.filter(id = pk)
    def list(self,request):
        print('get')
        tag_serializer = self.serializer_class(self.get_queryset(),many = True)
        return Response(tag_serializer.data,status = status.HTTP_200_OK)
    def retrieve(self,request,pk =None):
        print('retrieve')
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
            
            tagSave = tag_serializer.save()

            #seteando el registro del historial
            #setHistory(tagSave,'agregar tag nuevo',1)
            '''history = tagSave.historical.create(id = tagSave.id,tagName = tagSave.tagName, fechaRegistro = tagSave.fechaRegistro
                                                ,fechaUpdate = tagSave.fechaUpdate
                                                ,history_date = datetime.today(),history_change_reason = "last",history_type = '+',history_user_id = 1)
            history.save()'''
            return Response({'mensaje':'Se registros correctamente el tag'},status = status.HTTP_200_OK)
        else:
            return Response(tag_serializer.errors,status = status.HTTP_400_BAD_REQUEST)

    def update(self,request,pk=None):
        tag = self.get_queryset(pk).first()
        if tag:
            tag_serializer = self.serializer_class(tag , data = request.data)
            if tag_serializer.is_valid():
                tagUpdate = tag_serializer.save()
                #setHistory(tagUpdate,'actualizo tag',1)
                return Response({'mensaje':'Se actualizo correctamente el tag'},status = status.HTTP_200_OK)
            return Response(tag_serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        return Response({'error':'No existe el tag'},status = status.HTTP_400_BAD_REQUEST)
            
    
     
