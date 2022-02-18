from apps.file.models import File
from apps.folder.models import Folder
from rest_framework.response import Response
from rest_framework import status
from apps.file.api.serializers.file_serializers import FileCreateSerializer,FileObtenerSerializer,FileFolderCreateSerializer,FileDetalleSerializer,FileUpdateOcrSerializer
from apps.file.api.serializers.general_serializers import File_Serializer,FileInFolder_Serializer
from apps.users.authenticacion_mixings import Authentication
from django.contrib.sites.shortcuts import get_current_site
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from rest_framework import viewsets
from django.http import FileResponse
from apps.base.util import DocumentoOCR
import threading
import PyPDF2
#import pdfplumber
#from apps.base.pdfConvertPdfMiner import extrarText
from django.utils.crypto import get_random_string
#import fitz


def guardarOcr(file,id):
    documentoRenderisado = DocumentoOCR(file)
    text = str(documentoRenderisado.obtenerTexto())
    file = FileUpdateOcrSerializer(File.objects.filter(id = id).first(),data = {'contenidoOCR':text})
    if file.is_valid():
        file.save()
def extraerExtencion(Archivo):
    extension = [["jpg","application/jpeg"],["png","application/png"],["xlsx","application/vnd.ms-excel"],["docx","application/msword"],["pptx","application/vnd.ms-powerpoint"],["pdf","application/pdf"]]
    ext,aplication = None,None
    for e in extension:
        if e[0] in Archivo:
            ext = e[0]
            aplication =e[1]
    return ext,aplication 

class FileObtenerViewSet(Authentication,viewsets.GenericViewSet):
    serializer_class = FileObtenerSerializer
    def get_queryset(self,pk=None):
        if pk is None:
            return None
        return self.serializer_class().Meta.model.objects.filter(slug=pk,unidadArea_id = self.userFull.unidadArea_id).first()
    
    def retrieve(self,request,pk=None):

        documento_query = self.get_queryset(pk)
        if documento_query:
            documento = File_Serializer().Meta.model.objects.filter(slug=pk,unidadArea_id = self.userFull.unidadArea_id).first()
            if documento:
               
                doc = str(documento.documento_file)#56 en linux / 34 windows
                file_location =  settings.MEDIA_ROOT + 'files/' + doc 
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
            response = Response({'error':'No existe el documento o archivo solicitado'},status = status.HTTP_400_BAD_REQUEST)
        
        return Response({'error':'Error al procesar la solicitud'},status = status.HTTP_400_BAD_REQUEST)
class FileViewSet(Authentication,viewsets.GenericViewSet):
    
    serializer_class = FileFolderCreateSerializer

    def get_queryset(self,pk=None):
        if pk is None:
            return FileCreateSerializer().Meta.model.objects.filter(unidadArea_id = self.userFull.unidadArea_id)
        return FileCreateSerializer().Meta.model.objects.filter(slug=pk,unidadArea_id = self.userFull.unidadArea_id).first()
    def list(self,request):

        print(self.userFull.unidadArea_id)
        documento_serializer = FileDetalleSerializer(self.get_queryset(),many = True)
        return Response(documento_serializer.data,status = status.HTTP_200_OK)

    

    def create(self,request):
        documento_serializer = self.serializer_class(data = request.data)
        
        if documento_serializer.is_valid():
            if Folder.objects.filter(slug = documento_serializer.validated_data['directorioslug'],unidadArea_id = self.userFull.unidadArea_id):

                current_site = get_current_site(request).domain
                ruta = settings.MEDIA_ROOT+'files/'
                fs = FileSystemStorage(location=ruta)
                file = fs.save(request.FILES['documento_file'].name.replace(" ","_"),request.FILES['documento_file'])
                fileurl = fs.url(file)

                doc = fileurl[1:]
                documento_serializer.validated_data['documento_file'] = doc

                documento = documento_serializer.save()
                documento.extension,application = extraerExtencion(fileurl[1:])
                documento.slug = get_random_string(length=11)
                documento.unidadArea_id = self.userFull.unidadArea_id
                mensaje = "Documento cargado exitosamente"
                #documentoOcr = DocumentoOCR(fileurl)
                textPDF = obtenerTextoPDF(fileurl)
                documento.contenidoOCR = textPDF #documentoOcr.obtenerTexto()
                if textPDF == "":
                    mensaje = 'Documento cargado exitosamente, se estra procesando el contenido del archivo...' 
                    threading_text = threading.Thread(target=guardarOcr,args=(fileurl,documento.id,))
                    threading_text.start()
                    print('Cantidad de threading : ',threading.active_count())
                documento.save()
                parentID = Folder.objects.filter(slug = request.data['directorioslug']).first()
                if parentID:

                    fileinfoler_serializer = FileInFolder_Serializer(data = {
                        'file': documento.id,
                        'parent_folder':parentID.id#Folder.objects.filter(slug = request.data['directorioslug']).first().id
                    })
                    if fileinfoler_serializer.is_valid():
                        fileinfoler_serializer.save()

                    '''threading_text = threading.Thread(target=guardarOcr,args=(fileurl,documento.id,))
                    threading_text.start()
                    print('Cantidad de threading : ',threading.active_count())'''
                    return Response({'Mensaje':mensaje},status = status.HTTP_200_OK)
                #File.objects.filter(id = documento.id).delete()
                return Response({'error':'La carpeta contenedora no existe'},status = status.HTTP_404_NOT_FOUND)
            return Response({'error':'La carpeta contenedora no existe'},status = status.HTTP_401_UNAUTHORIZED)       
        else:
            #return Response({'Error':'no se pudo cargar el documento'},status = status.HTTP_400_BAD_REQUEST)
            return Response(documento_serializer.errors,status = status.HTTP_400_BAD_REQUEST)
    def retrieve(self,request,pk=None):
        documento = FileDetalleSerializer(self.get_queryset(pk))
        if documento:
            return Response(documento.data,status=status.HTTP_200_OK)
        return Response({'error':'No existe el documento solicitado'},status = status.HTTP_404_NOT_FOUND)
    def update(self,request,pk=None):
        documento = self.get_queryset(pk)
        if documento:
            documento_serializer = self.serializer_class(documento,data = request.data)
            if documento_serializer.is_valid():
                documento_serializer.save()
                return Response({'mensaje':'Documento actualizado correctamente'},status = status.HTTP_200_OK)                
            return Response({'error':'hubo un error al actualizar los datos'},status = status.HTTP_400_BAD_REQUEST)
        return Response({'error':'No existe el documento'},status = status.HTTP_400_BAD_REQUEST)


def obtenerTextoPDF(file):
        text =""
        
        '''with pdfplumber.open(settings.MEDIA_ROOT+'files'+file) as pdf:
            pdf.strict = True
            totalpages = len(pdf.pages)
            for x in range(0,totalpages):
                first_page = pdf.pages[x]
                text = text + str(first_page.extract_text().replace("",''))
                percent = ((x+1)*100)/totalpages
                print(str(round(percent,2))+" %")
                #print(first_page.extract_text().replace("",''))
        return text'''
        #documentoRenderisado = DocumentoOCR(file)
        try:

            pdfFileObj = open(settings.MEDIA_ROOT +'files'+file,'rb')
            
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj,  strict = False)
            
            print(pdfReader.isEncrypted)
            print(pdfReader.numPages)
            #print(pdfReader.getPage(0).extractText())
            for x in range(0, pdfReader.numPages):
                pageObj = pdfReader.getPage(x)
                #print(pageObj.extractText())
                text = text + str(pageObj.extractText())
                percent = ((x+1)*100)/pdfReader.numPages
                print(str(round(percent,2))+" %")
            return text 
        except:
            return None


        '''text = extrarText(file)
        return text'''
        #text = str(documentoRenderisado.obtenerTexto())
