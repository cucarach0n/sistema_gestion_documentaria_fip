from apps.adminutils.api.serializers.disk_serializers import DiskSerializer
from rest_framework.response import Response
from rest_framework import status
from apps.users.authenticacion_mixings import Authentication
from rest_framework import viewsets
import psutil
import platform

def to_gb(bytes):
    "Convierte bytes a gigabytes."
    return bytes / 1024**3
def to_mb(bytes):
    "Convierte bytes a megabytes."
    return bytes / 1024**2

class DiskViewSet(Authentication,viewsets.GenericViewSet):

    serializer_class = DiskSerializer
    def get_queryset(self):
        sistema = platform.system()
        if(sistema == "Linux"):
            disk_usage = psutil.disk_usage("/")
        else:
            disk_usage = psutil.disk_usage("C:\\")
        total = "{:.2f}".format(to_gb(disk_usage.total))
        libre = "{:.2f}".format(to_gb(disk_usage.free))
        usado = "{:.2f}".format(to_gb(disk_usage.used))
        usadoPorcentaje = "{}".format(disk_usage.percent)
        unidadMedida = "Gb"
        data = {
            "espacioTotal":total,
            "espacioLibre":libre,
            "espacioUtilizado":usado,
            "espacioUtilizadoPorcentaje":usadoPorcentaje,
            "unidadMedida":unidadMedida
        }
        return data
    

    def list(self,request):
        if(self.userFull.is_superuser):
            serializer = self.get_serializer(data=self.get_queryset())
            if(serializer.is_valid()):
                return Response(serializer.validated_data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response({"error":"Acceso denegado"},status=status.HTTP_403_FORBIDDEN)