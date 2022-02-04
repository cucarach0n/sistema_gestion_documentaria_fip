
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from apps.sgdapi.api.serializers.documento_serializers import DocumentoCreateSerializer
from apps.sgdapi.api.serializers.general_serializers import DocumentoOcrSerializer
from datetime import datetime
from pathlib import Path
from django.core.files.storage import FileSystemStorage

from apps.sgdapi.util import DocumentoOCR
#get/post
class DocumentoCreateAPIView(generics.ListCreateAPIView):
    serializer_class = DocumentoCreateSerializer

    queryset = DocumentoCreateSerializer.Meta.model.objects.all()
    
    def post(self,request):
        documento_serializer = self.serializer_class(data = request.data)
        
        if documento_serializer.is_valid():
            print(request.FILES['documento_file'])
            fs = FileSystemStorage()
            file = fs.save(request.FILES['documento_file'].name,request.FILES['documento_file'])
            fileurl = fs.url(file)
            print(fileurl)
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

