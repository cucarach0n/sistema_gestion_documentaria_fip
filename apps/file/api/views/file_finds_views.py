# -*- coding: utf-8 -*-
from distutils import extension
from hashlib import new
from apps.file.api.serializers.file_serializers import FileBuscarAvanzadoSerializer, FileDetalleSerializer
from rest_framework.response import Response
from rest_framework import status
from apps.users.authenticacion_mixings import Authentication
from rest_framework import viewsets


from django.db.models import Q
from django.core.paginator import Paginator
import datetime
from datetime import date
from datetime import timedelta
def generarRangoFecha(opcion):
    today =date.today()
    newFecha = None
    rango = []
    #hoy
    if opcion == 1:
        newFecha = today 
    #ayer
    elif opcion == 2:
        newFecha = today - timedelta(days=1)
    #semana
    elif opcion == 3:
        newFecha = today - timedelta(days=7)
    #mes
    elif opcion == 4:
        newFecha = today - timedelta(days=30)
    rango.append(newFecha)
    rango.append(today)
    return rango
        

class FileBuscarAvanzadoAPIView(Authentication,viewsets.GenericViewSet):

    serializer_class = FileBuscarAvanzadoSerializer
    def get_queryset(self,data):
        if(self.userFull.is_staff < 3):
            if data['opcionFecha'] == None:
                print("opcion fecha none")
                print(data['tipoDoc'])
                if data['tipoCaracteristicaId'] == None:
                    return self.get_serializer().Meta.model.objects.filter(Q(scope =True,unidadArea_id=self.userFull.unidadArea_id,eliminado = False)|
                                                                        Q(scope =False,user_id=self.userFull.id,eliminado = False),
                                                                        Q(contenidoOCR__icontains = data['numeroECS'])|Q(contenidoOCR__isnull = True),
                                                                        #contenidoOCR__icontains = data['numeroECS'],
                                                                        extension__icontains = data['tipoDoc'],
                                                                        nombreDocumento__icontains = data['nombreDoc'],
                                                                        fileinfolder__parent_folder__slug__icontains = data['carpetaSlug']).distinct()
                print("opcion fecha none siguiente return")
                return self.get_serializer().Meta.model.objects.filter(Q(scope =True,unidadArea_id=self.userFull.unidadArea_id,eliminado = False)|
                                                                        Q(scope =False,user_id=self.userFull.id,eliminado = False),
                                                                        Q(contenidoOCR__icontains = data['numeroECS'])|Q(contenidoOCR__isnull = True),
                                                                        #contenidoOCR__icontains = data['numeroECS'],
                                                                        extension__icontains = data['tipoDoc'],
                                                                        nombreDocumento__icontains = data['nombreDoc'],
                                                                        fileinfolder__parent_folder__slug__icontains = data['carpetaSlug'],
                                                                        caracteristicafile__caracteristica__tipoCaracteristica__id = data['tipoCaracteristicaId'],
                                                                        caracteristicafile__caracteristica__nombreCaracteristica__icontains = data['nombreCaracteristica']).distinct()
            else:
                if data['fechaInicio'] == None and data['fechaFin'] == None:
                    rango = generarRangoFecha(data['opcionFecha'])
                else:
                    rango = [data['fechaInicio'],data['fechaFin']]
                return self.get_serializer().Meta.model.objects.filter(Q(scope =True,unidadArea_id=self.userFull.unidadArea_id,eliminado = False)|
                                                                    Q(scope =False,user_id=self.userFull.id,eliminado = False),
                                                                    Q(contenidoOCR__icontains = data['numeroECS'])|Q(contenidoOCR__isnull = True),
                                                                    #contenidoOCR__icontains = data['numeroECS'],
                                                                    extension__icontains = data['tipoDoc'],
                                                                    nombreDocumento__icontains = data['nombreDoc'],
                                                                    fileinfolder__parent_folder__slug__icontains = data['carpetaSlug'],
                                                                    fileinfolder__fechaCreacion__date__range = [rango[0],rango[1]]).order_by('fileinfolder__fechaCreacion').distinct()
            '''else:
                return self.get_serializer().Meta.model.objects.filter(Q(nombreDocumento__icontains = data['nombreDoc'])| 
                                                                    Q(contenidoOCR__icontains = data['numeroExpediente'])| 
                                                                    Q(contenidoOCR__icontains = data['numeroCompra'])| 
                                                                    Q(contenidoOCR__icontains = data['numeroServicio']),
                                                                    Q(scope =True,unidadArea_id=self.userFull.unidadArea_id,eliminado = False)|
                                                                    Q(scope =False,user_id=self.userFull.id,eliminado = False),
                                                                    extension__icontains = data['tipoDoc'],
                                                                    fileinfolder__parent_folder__nombre__icontains = data['carpetaNombre'],
                                                                    fileinfolder__fechaCreacion__date__range = [data['fechaInicio'],data['fechaFin']]).distinct()'''
        if data['opcionFecha'] == None:
            print("opcion fecha none")
            print(data['tipoDoc'])
            if data['tipoCaracteristicaId'] == None:
                return self.get_serializer().Meta.model.objects.filter(Q(contenidoOCR__icontains = data['numeroECS'])|Q(contenidoOCR__isnull = True),
                                                                    scope =True,eliminado = False,
                                                                    #contenidoOCR__icontains = data['numeroECS'],
                                                                    extension__icontains = data['tipoDoc'],
                                                                    nombreDocumento__icontains = data['nombreDoc'],
                                                                    fileinfolder__parent_folder__slug__icontains = data['carpetaSlug']).distinct()
            print("opcion fecha none siguiente return")
            return self.get_serializer().Meta.model.objects.filter(Q(contenidoOCR__icontains = data['numeroECS'])|Q(contenidoOCR__isnull = True),
                                                                    #contenidoOCR__icontains = data['numeroECS'],
                                                                    scope =True,eliminado = False,
                                                                    extension__icontains = data['tipoDoc'],
                                                                    nombreDocumento__icontains = data['nombreDoc'],
                                                                    fileinfolder__parent_folder__slug__icontains = data['carpetaSlug'],
                                                                    caracteristicafile__caracteristica__tipoCaracteristica__id = data['tipoCaracteristicaId'],
                                                                    caracteristicafile__caracteristica__nombreCaracteristica__icontains = data['nombreCaracteristica']).distinct()
        else:
            if data['fechaInicio'] == None and data['fechaFin'] == None:
                rango = generarRangoFecha(data['opcionFecha'])
            else:
                rango = [data['fechaInicio'],data['fechaFin']]
            return self.get_serializer().Meta.model.objects.filter(Q(contenidoOCR__icontains = data['numeroECS'])|Q(contenidoOCR__isnull = True),
                                                                #contenidoOCR__icontains = data['numeroECS'],
                                                                scope =True,eliminado = False,
                                                                extension__icontains = data['tipoDoc'],
                                                                nombreDocumento__icontains = data['nombreDoc'],
                                                                fileinfolder__parent_folder__slug__icontains = data['carpetaSlug'],
                                                                fileinfolder__fechaCreacion__date__range = [rango[0],rango[1]]).order_by('fileinfolder__fechaCreacion').distinct()
        '''else:
            return self.get_serializer().Meta.model.objects.filter(Q(nombreDocumento__icontains = data['nombreDoc'])| 
                                                                Q(contenidoOCR__icontains = data['numeroExpediente'])| 
                                                                Q(contenidoOCR__icontains = data['numeroCompra'])| 
                                                                Q(contenidoOCR__icontains = data['numeroServicio']),
                                                                Q(scope =True,unidadArea_id=self.userFull.unidadArea_id,eliminado = False)|
                                                                Q(scope =False,user_id=self.userFull.id,eliminado = False),
                                                                extension__icontains = data['tipoDoc'],
                                                                fileinfolder__parent_folder__nombre__icontains = data['carpetaNombre'],
                                                                fileinfolder__fechaCreacion__date__range = [data['fechaInicio'],data['fechaFin']]).distinct()'''
        
    def create(self,request):
        file_serializer = self.get_serializer(data = request.data)
        if file_serializer.is_valid():
            result = self.get_queryset(file_serializer.validated_data)
            fileBusqueda_serializer = FileDetalleSerializer(result,many = True)
            return Response(fileBusqueda_serializer.data,status = status.HTTP_200_OK)
        else:
            return Response(file_serializer.errors,status = status.HTTP_400_BAD_REQUEST)