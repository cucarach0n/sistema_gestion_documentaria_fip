
from apps.folder.models import Folder
from rest_framework.response import Response
from rest_framework import status
from apps.folder.api.serializers.folder_serializer import (
    FolderSerializer,
    FolderDirecotorioListSerializer,
    FolderDeleteSerializer,
    FolderUpdateSerializer,
    FolderHistorySerializer
    )
from apps.users.authenticacion_mixings import Authentication
import os
from django.conf import settings
from rest_framework import viewsets
from django.utils.crypto import get_random_string  


class FolderViewSet(Authentication,viewsets.GenericViewSet):
    serializer_class = FolderSerializer

    def get_queryset(self,pk = None):
        if pk is None:
            return self.serializer_class().Meta.model.objects.filter(carpeta_hija__isnull =True,unidadArea_id = self.userFull.unidadArea_id)
        else:
            try:
                return self.serializer_class().Meta.model.objects.filter(slug = pk,unidadArea_id = self.userFull.unidadArea_id)
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
        #if self.userFull.is_superuser == 1 :
        folder_serializer = self.serializer_class(data = request.data)
        if folder_serializer.is_valid():
            folder_serializer.validated_data['slug'] = get_random_string(length=11)
            #folder_serializer.validated_data['unidadArea'] = self.userFull.unidadArea_id
            '''try:
                os.makedirs(settings.MEDIA_ROOT + "files/"  + folder_serializer.validated_data['slug'] , exist_ok=True)
            except:
                print('Error al crear el directorio')
                Response({'error':"Hubo un error al crear el directorio"},status = status.HTTP_400_BAD_REQUEST)'''
            folder_serializer.save()
            
            return Response({'Mensaje':"Se creo correctamente el directorio"},status = status.HTTP_200_OK)
        else:
            return Response(folder_serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        #return Response({'error':"Acceso denegado"},status = status.HTTP_401_UNAUTHORIZED)

        
class FolderDeleteAPIView(Authentication,viewsets.GenericViewSet):
    serializer_class = FolderDeleteSerializer
    def get_queryset(self,pk = None):
        return self.get_serializer().Meta.model.objects.filter(slug = pk).first()
    
    def destroy(self,request,pk = None):
        folderSerializer = self.get_serializer(data = request.data)
        if folderSerializer.is_valid():
            if self.userFull.is_superuser:
                folderDeleteResult = self.get_queryset(pk)
                folderDeleteResult.delete()
                return Response({'Mensaje':'Folder eliminado correctamente'},status = status.HTTP_200_OK)
            else:
                return Response({'Error':'No permitido'},status = status.HTTP_400_BAD_REQUEST)  
        else:
            return Response(folderSerializer.errors,status = status.HTTP_400_BAD_REQUEST) 
class FolderUpdateAPIView(Authentication,viewsets.GenericViewSet):
    serializer_class = FolderUpdateSerializer
    def get_queryset(self,pk = None):
        return self.get_serializer().Meta.model.objects.filter(slug = pk).first()
    def update(self,request,pk = None):
        if self.get_queryset(pk):
            folderUpdateSerializer = self.get_serializer(self.get_queryset(pk),data = request.data)
            if folderUpdateSerializer.is_valid():
                folderUpdateSerializer.save()
                return Response({'Mensaje':'Folder actualizado correctamente'},status = status.HTTP_200_OK)
            else:
                return Response(folderUpdateSerializer.errors,status = status.HTTP_400_BAD_REQUEST)
        else:
             return Response({'Error':'El folder no existe'},status = status.HTTP_200_OK)

class FolderHistoryAPIView(Authentication,viewsets.GenericViewSet):
    serializer_class = FolderHistorySerializer
    def get_queryset(self,pk=None):
        return Folder.historical.filter(id = pk,history_user_id=self.userFull.id)
    
    def retrieve(self,request,pk = None):
        historyFolder = self.get_queryset(Folder.objects.get(slug = pk).id)
        folderHistorialSerializer = self.get_serializer(historyFolder,many = True)
        return Response(folderHistorialSerializer.data, status = status.HTTP_200_OK)



