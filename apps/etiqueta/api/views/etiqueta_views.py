from apps.etiqueta.api.serializers.general_serializers import EtiquetaSerializer
from apps.etiqueta.models import Etiqueta
from apps.file.models import File
from rest_framework.response import Response
from rest_framework import status
from apps.etiqueta.api.serializers.etiqueta_serializers import EtiquetaCreateSerializer,EtiquetaBuscarSerializer, EtiquetaListSerializer, EtiquetaUpdateSerializer
from apps.users.authenticacion_mixings import Authentication
from rest_framework import viewsets


class EtiquetaCreateViewSet(Authentication,viewsets.GenericViewSet):
    serializer_class = EtiquetaCreateSerializer
    def get_queryset(self,pk):
        return Etiqueta.objects.get(id = pk,user_id = self.userFull.id)
    def create(self,request):
        etiquetaSerializer = self.get_serializer(data = request.data,context = {'userId':self.userFull.id,'fileSlug':request.data['slugFile'],'idUnidadArea':self.userFull.unidadArea_id})
        if etiquetaSerializer.is_valid():
            #etiquetaSerializer.validated_data['user_id'] = self.user.id
            etiquetaCreado = etiquetaSerializer.save()
            etiquetaCreatedSerializer= EtiquetaListSerializer(etiquetaCreado)
            return Response(etiquetaCreatedSerializer.data,status = status.HTTP_200_OK)
        return Response(etiquetaSerializer.errors,status = status.HTTP_400_BAD_REQUEST)
    def destroy(self,request,pk):
        etiqueta = self.get_queryset(pk)
        if etiqueta:
            etiqueta.delete()
            return Response({'mensaje':'etiqueta eliminado correctamente'},status = status.HTTP_200_OK)
        return Response({'error':'La etiqueta no existe'},status = status.HTTP_200_OK)
    
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
    
'''class EtiquedaEliminarViewSet(Authentication,viewsets.GenericViewSet):
    
    def get_queryset(self,pk):
        return Etiqueta.objects.get(id = pk,user_id = self.userFull.id)
    
    def delete(self,request,pk):
        etiqueta = self.get_queryset(pk)
        if etiqueta:
            etiqueta.delete()
            
            return Response({'mensaje':'etiqueta eliminado correctamente'},status = status.HTTP_200_OK)
        return Response({'error':'La etiqueta no existe'},status = status.HTTP_200_OK)'''
class EtiquetaUpdateViewSet(Authentication, viewsets.GenericViewSet):
    serializer_class = EtiquetaUpdateSerializer
    def get_queryset(self,pk = None):
        return self.get_serializer().Meta.model.objects.get(id = pk)
    
    def update(self,request,pk):
        etiqueta = self.get_queryset(pk)
        serializer = self.get_serializer(etiqueta,data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response({"mensaje":"actualizado correctamente"},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



