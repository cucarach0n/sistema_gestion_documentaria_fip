from apps.base.util import validarCompartido
from apps.file.api.serializers.file_serializers import FileDetalleShareSerializer
from apps.file.models import File, FileInFolder
from apps.folder.models import Folder
from apps.share.api.serializers.fileShare_serializers import FileShareCreateSerializer, FileShareValidateCreateSerializer
from rest_framework.response import Response
from rest_framework import status
from apps.users.authenticacion_mixings import Authentication
from rest_framework import viewsets
from django.conf import settings
from django.utils.crypto import get_random_string
from django.core.files.storage import FileSystemStorage
class FileShareCloneViewSet(Authentication,viewsets.GenericViewSet):
    serializer_class = FileShareCreateSerializer
    def get_queryset(self,pk):
        return File.objects.filter(fileshare__estado = True,fileshare__file__slug = pk,fileshare__userTo__id = self.userFull.id).first()
    def retrieve(self,request,pk):
        fileResult = self.get_queryset(pk)
        if fileResult:
            if File.objects.filter(user_id = self.userFull.id,scope=False,nombreDocumento = fileResult.nombreDocumento):
                return Response({'error':'El file ya existe'},status = status.HTTP_400_BAD_REQUEST)
            folderMaster = Folder.objects.filter(scope = False,
                                                unidadArea_id = self.userFull.unidadArea_id,
                                                user_id =self.userFull.id,
                                                carpeta_hija__isnull =True).first()
            rutaFile = settings.MEDIA_ROOT+'files/'
            fileObject = open(rutaFile+fileResult.documento_file.name, 'rb')
            fs = FileSystemStorage(location=rutaFile)
            fileSave = fs.save(fileResult.documento_file.name,fileObject)
            nameNewFile = fs.get_valid_name(fileSave)

            fileCreate = File.objects.create(slug = get_random_string(11),
                            nombreDocumento = fileResult.nombreDocumento,
                            contenidoOCR = fileResult.contenidoOCR,
                            documento_file = nameNewFile,
                            extension = fileResult.extension,
                            user_id=self.userFull.id,
                            scope=False,
                            unidadArea_id=self.userFull.unidadArea_id)
            FileInFolder.objects.create(file_id = fileCreate.id,parent_folder_id = folderMaster.id)
            return Response({'mensaje':'File clonado exitosamente'},status = status.HTTP_200_OK)
        return Response({"error":"El file no existe"},status = status.HTTP_400_BAD_REQUEST)    
class FileShareViewSet(Authentication,viewsets.GenericViewSet):
    serializer_class = FileShareCreateSerializer

    def get_queryset(self,pk = None):
        if pk is None:
            return File.objects.filter(fileshare__estado = True,fileshare__userTo_id = self.userFull.id)
        else:
            return File.objects.filter(fileshare__estado = True,fileshare__file__slug = pk,fileshare__userTo__id = self.userFull.id)
    def create(self,request):
        fileShareSerializer = self.get_serializer(data = request.data,context = {'userId':self.userFull.id,'unidadId':self.userFull.unidadArea_id})
        if fileShareSerializer.is_valid():
            fileShareValidateSerializer = FileShareValidateCreateSerializer(data = {
                'file':fileShareSerializer.validated_data['slugFile'],
                'userTo':fileShareSerializer.validated_data['correoTo'],
                'userFrom':self.userFull.id
            })
            if fileShareValidateSerializer.is_valid():

                '''folderCreate = FolderShare()
                folderCreate.folder_id = folderShareSerializer.validated_data['slugFolder']
                folderCreate.userFrom_id = self.userFull.id
                folderCreate.userTo_id = folderShareSerializer.validated_data['correoTo']
                folderCreate.save()'''
                fileShareValidateSerializer.save()
                return Response({'mensaje':'Se compartio exitosamente el file con el usuario'},status = status.HTTP_200_OK)
            return Response(fileShareValidateSerializer.errors,status = status.HTTP_400_BAD_REQUEST)
        return Response(fileShareSerializer.errors,status = status.HTTP_400_BAD_REQUEST)
    '''def list(self,request):
        fileAllShareSerialiser = FileDetalleSerializer(self.get_queryset(),many = True)        
        return Response(fileAllShareSerialiser.data,status = status.HTTP_200_OK)'''
    
    def retrieve(self,request,pk):
        
        fileResult = self.get_queryset(pk)
        if fileResult:
            fileSerializer = FileDetalleShareSerializer(fileResult,many = True,context = {'userId':self.userFull.id})      
            return Response(fileSerializer.data,status = status.HTTP_200_OK)
        return Response({'error':'El file no existe o no tiene acceso'},status = status.HTTP_400_BAD_REQUEST)
            