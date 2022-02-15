
from rest_framework.response import Response
from rest_framework import status
from apps.folder.api.serializers.folder_serializer import (
    FolderSerializer,
    FolderDirecotorioListSerializer
    )
from apps.users.authenticacion_mixings import Authentication
import os
from django.conf import settings
from rest_framework import viewsets
from django.utils.crypto import get_random_string  


class FolderViewSet(viewsets.GenericViewSet):
    serializer_class = FolderSerializer

    def get_queryset(self,pk = None):
        if pk is None:
            return self.serializer_class().Meta.model.objects.filter(carpeta_hija__isnull =True)
        else:
            try:
                return self.serializer_class().Meta.model.objects.filter(slug = pk)
            except:
                return None
    def list(self,request):

        folders = FolderDirecotorioListSerializer(self.get_queryset(),many = True)


        '''
        arbol = []
        sub = []
        nodo = None
        folders = FolderListSerializer(self.get_queryset(),many = True)
        for folder in folders.data:
            nodo = FolderListaEnlasada(folder['id'],folder['slug'],folder['nombre'],folder['fechaCreacion'])
            print('Slug a buscar : ' + nodo.slug)
            subNodos = FolderInFolder.objects.filter(parent_folder_id = nodo.id)
            if subNodos:
                for subNodo in subNodos:
                    sub.append(FolderListaEnlasada(subNodo.id,subNodo.slug,subNodo.child_folder_name,subNodo.fechaCreacion))
                    
                    print(subNodo.id)
                
                #nodo.lista = None
            else:
                nodo.lista = []
            nodo.lista = sub
            arbol.append(nodo)
            nodo = None     
            sub = []    
        '''    
        '''    
        for a in arbol:
            print(a.slug)
            if a.lista is not None:
                for b in a.getLista():
                    print("-"+b.slug)
        ''' 
        
        return Response(folders.data,status = status.HTTP_200_OK)
    def retrieve(self,request,pk=None):
        folder = self.get_queryset(pk)
        if folder:
            #print(folder.id)
            folders = FolderDirecotorioListSerializer(folder,many = True)
            return Response(folders.data,status = status.HTTP_200_OK)
        return Response({'error':"El directorio no existe"},status = status.HTTP_400_BAD_REQUEST)
    def create(self,request):
        
        folder_serializer = self.serializer_class(data = request.data)
        if folder_serializer.is_valid():
            folder_serializer.validated_data['slug'] = get_random_string(length=6)
            '''try:
                os.makedirs(settings.MEDIA_ROOT + "files/"  + folder_serializer.validated_data['slug'] , exist_ok=True)
            except:
                print('Error al crear el directorio')
                Response({'error':"Hubo un error al crear el directorio"},status = status.HTTP_400_BAD_REQUEST)'''
            folder_serializer.save()
            return Response({'Mensaje':"Se creo correctamente el directorio"},status = status.HTTP_200_OK)
        else:
            return Response(folder_serializer.errors,status = status.HTTP_400_BAD_REQUEST)

        