from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from apps.sgdapi.api.serializers.documento_serializers import DocumentoCreateSerializer,DocumentoObtenerSerializer
from apps.sgdapi.api.serializers.general_serializers import DocumentoOcrSerializer,DocumentoSerializer
from datetime import datetime
from apps.sgdapi.util import DocumentoOCR
from apps.users.authenticacion_mixings import Authentication
from django.contrib.sites.shortcuts import get_current_site
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound
from rest_framework import viewsets
from django.http import FileResponse

from django.utils.decorators import method_decorator
import json
def extraerExtencion(Archivo):
    extension = [["jpg","application/jpeg"],["png","application/png"],["xlsx","application/vnd.ms-excel"],["docx","application/msword"],["pptx","application/vnd.ms-powerpoint"],["pdf","application/pdf"]]
    ext,aplication = None,None
    for e in extension:
        if e[0] in Archivo:
            ext = e[0]
            aplication =e[1]
    return ext,aplication 

class DocumentoObtenerViewSet(Authentication,viewsets.GenericViewSet):
    serializer_class = DocumentoObtenerSerializer
    def get_queryset(self,pk=None):
        if pk is None:
            return None
        return self.serializer_class().Meta.model.objects.filter(id=pk).first()
    
    def retrieve(self,request,pk=None):

        documento_query = self.get_queryset(pk)
        if documento_query:
            documento = DocumentoSerializer().Meta.model.objects.filter(id=pk).first()
            if documento:
                print(documento.documento_file)
                doc = str(documento.documento_file)#56 en linux / 34 windows
                file_location =  settings.MEDIA_ROOT + 'files/' + doc 
                print('Obteniendo file de ' + file_location)
                try:    
                    #with open(file_location, 'r') as f:
                    #    file_data = f.read()
                    file_data = open(file_location, 'rb')
                    # sending response 
                    ext,app = extraerExtencion(str(documento.documento_file))#56 en linux/ 34 windows
                    response = FileResponse(file_data, content_type=app)
                
                    #response['Content-Length'] = file_data.size
                    response['Content-Disposition'] = 'attachment; filename="'+str(documento.documento_file)+'"'#56 en linux/ 34 windows
                except:
                    # handle file not exist case here
                    response = Response({'error':'Hubo un error al obtener el archivo'},status = status.HTTP_400_BAD_REQUEST)
                return response

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
            ruta = settings.MEDIA_ROOT+'files/'
            fs = FileSystemStorage(location=ruta)
            file = fs.save(request.FILES['documento_file'].name,request.FILES['documento_file'])
            fileurl = fs.url(file)
            

            print(fileurl)
            doc = fileurl[1:]
            #absURl = 'http://'+current_site+'/media/files/'+ doc
            documento_serializer.validated_data['documento_file'] = doc
            
            
            documentoRenderisado = DocumentoOCR(fileurl)
            text = str(documentoRenderisado.obtenerTexto())
            documento = documento_serializer.save()
            documento.extension,application = extraerExtencion(fileurl[7:])
            documento.save()
            #for ext in self.extension:
            #    if ext in fileurl:
            #        documento.extension = ext
            #        documento.save()
             
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