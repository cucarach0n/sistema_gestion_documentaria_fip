from apps.adminutils.api.serializers.utils_serializer import CuentasSerializer
from apps.file.models import File
from apps.folder.models import Folder
from apps.tag.models import Tag
from apps.unidadArea.models import UnidadArea
from apps.users.models import User
from rest_framework.response import Response
from rest_framework import status
from apps.users.authenticacion_mixings import Authentication
from rest_framework import viewsets
import os
from django.conf import settings
def to_tb(bytes):
    "Convierte bytes a gigabytes."
    return bytes / 1024**4
def to_gb(bytes):
    "Convierte bytes a gigabytes."
    return bytes / 1024**3
def to_mb(bytes):
    "Convierte bytes a megabytes."
    return bytes / 1024**2
def to_kb(bytes):
    "Convierte bytes a kilobytes."
    return bytes / 1024**1

class ContadorViewSet(Authentication,viewsets.GenericViewSet):

    serializer_class = CuentasSerializer
    def get_queryset(self):
        carpetas = Folder.objects.all().count()
        files = File.objects.all().count()
        usuarios = User.objects.all().count()
        gestiones = UnidadArea.objects.all().count()
        categorias = Tag.objects.all().count()
        '''fileSize = os.path.getsize(settings.MEDIA_ROOT+'files/')
        
        print(str(size(fileSize, system=si)))'''

        data = {
            "carpetas":carpetas,
            "files":files,
            "usuarios":usuarios,
            "gestiones":gestiones,
            "categorias":categorias
        }
        return data
    def list(self,request):
        if(self.userFull.is_superuser):
            serializer = self.get_serializer(data=self.get_queryset())
            if(serializer.is_valid()):
                return Response(serializer.validated_data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response({"error":"Acceso denegado"},status=status.HTTP_403_FORBIDDEN)

class TotalEspacioFileViewSet(Authentication,viewsets.GenericViewSet):
    def get_queryset(self):
        tama??o = 0
        Folderpath = settings.MEDIA_ROOT+'files/'
        for path, dirs, files in os.walk(Folderpath): 
            for f in files: 
                fp = os.path.join(path, f) 
                tama??o += os.path.getsize(fp) 
        return tama??o
    def list(self,request):
        if(self.userFull.is_superuser):
            print(self.get_queryset())
            tama??oBruto = self.get_queryset()
            unidadMedida = "Bytes"
            if(tama??oBruto < 1024**2):
                tama??o = to_kb(tama??oBruto)
                unidadMedida = "Kb"
            elif(tama??oBruto < 1024**3):
                tama??o = to_mb(tama??oBruto)
                unidadMedida = "Mb"
            elif(tama??oBruto < 1024**4):
                tama??o = to_gb(tama??oBruto)
                unidadMedida = "Gb"
            elif(tama??oBruto < 1024**5):
                tama??o = to_tb(tama??oBruto)
                unidadMedida = "Tb"
            return Response({"tama??o":"{:.2f}".format(tama??o),
                            "unidadMedida":unidadMedida},status=status.HTTP_200_OK)
        return Response({"error":"Acceso denegado"},status=status.HTTP_403_FORBIDDEN)