

from distutils import extension
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from apps.sgdapi.api.serializers.documento_serializers import DocumentoCreateSerializer
from apps.sgdapi.api.serializers.general_serializers import DocumentoOcrSerializer,DocumentoSerializer
from datetime import datetime
from apps.sgdapi.util import DocumentoOCR
from apps.users.authenticacion_mixings import Authentication
from django.contrib.sites.shortcuts import get_current_site
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from rest_framework import viewsets

class DocumentoViewSet(Authentication,viewsets.GenericViewSet):
    serializer_class = DocumentoCreateSerializer
    extension = ["jpg","png","xlsx","docx","pptx","pdf"]
    def get_queryset(self,pk=None):
        if pk is None:
            return self.serializer_class().Meta.model.objects.all()
        return self.serializer_class().Meta.model.objects.filter(id=pk).first()
    def list(self,request):
        documento_serializer = self.serializer_class(self.get_queryset(),many = True)
        return Response(documento_serializer.data,status = status.HTTP_200_OK)
    def create(self,request):
        documento_serializer = self.serializer_class(data = request.data)
        
        if documento_serializer.is_valid():
            current_site = get_current_site(request).domain
            #print(request.FILES['documento_file'])
            fs = FileSystemStorage(location='sgdfip_rest/media/files')
            file = fs.save(request.FILES['documento_file'].name,request.FILES['documento_file'])
            fileurl = fs.url(file)
            

            print(fileurl)
            doc = fileurl[6:]
            absURl = 'http://'+current_site+'/media/files'+ doc
            documento_serializer.validated_data['documento_file'] = absURl
            
            
            documentoRenderisado = DocumentoOCR(fileurl)
            text = str(documentoRenderisado.obtenerTexto())
            documento = documento_serializer.save()
            for ext in self.extension:
                if ext in fileurl:
                    documento.extension = ext
                    documento.save()
             
            documentoOCR = {
                'contenido' : text,
                'fechaRegistro' : datetime.today().strftime('%Y-%m-%d'),
                'documento': documento.id
            }
            documentoOcrSerializer = DocumentoOcrSerializer(data = documentoOCR)
            if documentoOcrSerializer.is_valid():
                documentoOcrSerializer.save()
            

            #print(text)
            
            return Response({'Mensaje':'Documento cargado exitosamente'},status = status.HTTP_200_OK)
        else:
            return Response({'Error':'no se pudo cargar el documento'},status = status.HTTP_400_BAD_REQUEST)

    def retrieve(self,request,pk=None):
        documento = self.get_queryset(pk)
        if documento:
            documento_serializer = self.serializer_class(documento)
            return Response(documento_serializer.data,status=status.HTTP_200_OK)
        return Response({'error':'No existe el documento solicitado'})
    def update(self,request,pk=None):
        documento = self.get_queryset(pk)
        if documento:
            documento_serializer = self.serializer_class(documento,data = request.data)
            if documento_serializer.is_valid():
                documento_serializer.save()
                return Response({'mensaje':'Documento actualizado correctamente'},status = status.HTTP_200_OK)                
            return Response({'error':'hubo un error al actualizar los datos'},status = status.HTTP_400_BAD_REQUEST)
        return Response({'error':'No existe el documento'},status = status.HTTP_400_BAD_REQUEST)




'''
class DocumentoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DocumentoSerializer

    queryset = DocumentoSerializer.Meta.model.objects.all()
    def query_set(self,pk = None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(estado = 1)
        else:
            return self.get_serializer().Meta.model.objects.filter(id = pk,estado = 1)


    def patch(self,request,pk = None):
        if self.get_queryset(pk):
            documento_serializer = self.serializer_class(self.get_queryset(pk))
            return Response(documento_serializer.data,status = status.HTTP_200_OK)
        else:
            return Response({'error':'No existe un documento con estos datos'},status = status.HTTP_400_BAD_REQUEST)
        
    def put(self,request,pk = None):
        if self.get_queryset(pk):
            documento_serializer = self.serializer_class(self.get_queryset(pk),data = request.data)
            if documento_serializer.is_valid():
                documento_serializer.save()
                return Response(documento_serializer.data,status = status.HTTP_200_OK)
        return Response(documento_serializer.errors,status = status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk = None):
        documento = self.get_queryset().filter(id = pk).firts()
        if documento:
            documento.estado = 0
            documento.save()
            return Response({'mensaje':'documento eliminado correctamente'},status = status.HTTP_200_OK)
        return Response({'error':'No existe un documento con estos datos'},status = status.HTTP_400_BAD_REQUEST)

#get/post/Authentication,
class DocumentoCreateAPIView(Authentication,generics.ListCreateAPIView):
    serializer_class = DocumentoCreateSerializer

    queryset = DocumentoCreateSerializer.Meta.model.objects.all()
    
    def post(self,request):
        documento_serializer = self.serializer_class(data = request.data)
        
        if documento_serializer.is_valid():
            current_site = get_current_site(request).domain
            #print(request.FILES['documento_file'])
            fs = FileSystemStorage(location='sgdfip_rest/media/files')
            file = fs.save(request.FILES['documento_file'].name,request.FILES['documento_file'])
            fileurl = fs.url(file)
            print(fileurl)
            doc = fileurl[6:]
            absURl = 'http://'+current_site+'/media/files'+ doc
            documento_serializer.validated_data['documento_file'] = absURl

            documentoRenderisado = DocumentoOCR(fileurl)
            text = str(documentoRenderisado.obtenerTexto())
            documento = documento_serializer.save()
            documentoOCR = {
                'contenido' : text,
                'fechaRegistro' : datetime.today().strftime('%Y-%m-%d'),
                'documento': documento.id
            }
            documentoOcrSerializer = DocumentoOcrSerializer(data = documentoOCR)
            if documentoOcrSerializer.is_valid():
                documentoOcrSerializer.save()
            

            #print(text)
            
            return Response({'Mensaje':'Documento cargado exitosamente'},status = status.HTTP_200_OK)
        else:
            return Response({'Error':'no se pudo cargar el documento'},status = status.HTTP_400_BAD_REQUEST)

'''