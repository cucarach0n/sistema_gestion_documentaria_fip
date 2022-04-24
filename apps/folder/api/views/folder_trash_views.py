from apps.base.util import setDestruirHijos, setEliminarHijos
from apps.file.api.serializers.file_serializers import FileDetalleSerializer
from apps.folder.api.serializers.treefolder_serializer import TreeFolderSerializer
from apps.folder.models import Folder, FolderInFolder
from rest_framework.response import Response
from rest_framework import status
from apps.folder.api.serializers.folder_serializer import (
    FolderDeleteSerializer,
    FolderTrashPublicListSerializer
    )
from apps.file.models import File
from apps.users.authenticacion_mixings import Authentication
from rest_framework import viewsets

class FolderQuitPublicAPIView(Authentication,viewsets.GenericViewSet):
    serializer_class = FolderDeleteSerializer
    def get_queryset(self,pk = None):
        return self.get_serializer().Meta.model.objects.filter(slug = pk,scope = True,unidadArea_id = self.userFull.unidadArea_id).first()
    
    def retrieve(self,request,pk = None):
        folderResult = self.get_queryset(pk)
        if folderResult:
            if folderResult.eliminado ==True:
                setDestruirHijos(folderResult.slug)
                folderResult.delete()
                return Response({'Mensaje':'Folder destruido correctamente'},status = status.HTTP_200_OK)
            folderMasterPublic = Folder.objects.get(user__is_superuser = True,
                                                    carpeta_hija__isnull =True,
                                                    unidadArea_id = self.userFull.unidadArea_id,eliminado = False)
            setEliminarHijos(folderResult.slug)
            FolderInFolder.objects.filter(child_folder_id = folderResult.id).update(parent_folder_id = folderMasterPublic.id)
            File.objects.filter(fileinfolder__parent_folder_id = folderResult.id).update(eliminado = True)                                        
            folderResult.eliminado = True
            folderResult.save()
            '''FolderTrash.objects.create(
                folder_id = folderResult.id,
                user_id = self.userFull.id
            )'''
            return Response({'Mensaje':'Folder eliminado correctamente'},status = status.HTTP_200_OK)
        return Response({'mensaje':'La carpeta no existe'},status = status.HTTP_400_BAD_REQUEST)
class FolderRestaurarPublicAPIView(Authentication,viewsets.GenericViewSet):
    serializer_class = FolderDeleteSerializer
    def get_queryset(self,pk = None):
        return self.get_serializer().Meta.model.objects.filter(slug = pk,scope = True,eliminado = True,unidadArea_id = self.userFull.unidadArea_id).first()
    
    def retrieve(self,request,pk = None):
        folderResult = self.get_queryset(pk)
        if folderResult:
            #if self.userFull.is_staff < 3:
            folderMasterPublic = Folder.objects.get(user__is_superuser = True,
                                                carpeta_hija__isnull =True,
                                                unidadArea_id = self.userFull.unidadArea_id,eliminado = False,scope = True)
            setEliminarHijos(folderResult.slug,False)
            FolderInFolder.objects.filter(child_folder_id = folderResult.id).update(parent_folder_id = folderMasterPublic.id)
            File.objects.filter(fileinfolder__parent_folder_id = folderResult.id).update(eliminado = False)                                        
            folderResult.eliminado = False
            folderResult.save()
            '''FolderTrash.objects.create(
                folder_id = folderResult.id,
                user_id = self.userFull.id
            )'''
            
            
            return Response({'Mensaje':'Folder restaurado en la carpeta '+ folderMasterPublic.nombre},status = status.HTTP_200_OK)
            #return Response({'Error':'No permitido'},status = status.HTTP_401_UNAUTHORIZED)  
        return Response({'mensaje':'La carpeta no existe o no esta eliminada'},status = status.HTTP_400_BAD_REQUEST)
class FolderTrashPublicAPIView(Authentication,viewsets.GenericViewSet):
    serializer_class = FolderTrashPublicListSerializer  
    def get_queryset(self,pk = None):
        if pk is not None:
            
            return self.get_serializer().Meta.model.objects.filter(slug = pk,eliminado = True,scope = True,unidadArea_id = self.userFull.unidadArea_id).first()
        folderMasterPublic = Folder.objects.get(user__is_superuser = True,
                                                carpeta_hija__isnull =True,
                                                unidadArea_id = self.userFull.unidadArea_id,eliminado = False,scope = True)
        return self.get_serializer().Meta.model.objects.filter(carpeta_hija__parent_folder_id = folderMasterPublic.id,eliminado = True,unidadArea_id = self.userFull.unidadArea_id)
    def list(self,request):
        #if self.userFull.is_staff < 3:
        folderMasterPublic = Folder.objects.get(user__is_superuser = True,
                                            carpeta_hija__isnull =True,
                                            unidadArea_id = self.userFull.unidadArea_id,eliminado = False,scope = True)

        folders = self.get_serializer(self.get_queryset(),many = True,context = {'userId':self.userFull.id,'userStaff': self.userFull.is_staff})

        fileSerializer = FileDetalleSerializer(File.objects.filter(fileinfolder__parent_folder_id = folderMasterPublic.id,
                                                        eliminado = True,
                                                        unidadArea_id = self.userFull.unidadArea_id),many = True,context = {'userId':self.userFull.id})
        arbol = TreeFolderSerializer(self.get_queryset(),many = True)
        #return Response(folders.data,status = status.HTTP_200_OK)
        return Response({'nombre':'Papelera',
                        'subDirectorios':folders.data,
                        'files':fileSerializer.data,
                        'treefolders':arbol.data },status = status.HTTP_200_OK)
        #return Response({'error':'No permitido'},status = status.HTTP_400_BAD_REQUEST)
    def retrieve(self,request,pk):
        #if self.userFull.is_staff < 3:
        folder = self.get_queryset(pk)
        if folder:
            if folder.eliminado == False:
                return Response({'error':'La carpeta solicitada no esta eliminado'},status = status.HTTP_401_UNAUTHORIZED)
            folderSerializer = self.get_serializer(folder,context = {'userId':self.userFull.id,'userStaff': self.userFull.is_staff})
            return Response(folderSerializer.data,status = status.HTTP_200_OK)
        return Response({'mensaje':'La carpeta no existe'},status = status.HTTP_400_BAD_REQUEST)
        #return Response({'error':'No permitido'},status = status.HTTP_400_BAD_REQUEST)