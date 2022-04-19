
from apps.base.util import createHistory, setDestruirHijos, setEliminarHijos, setHistory, setPublicHijos, validarPrivado
from apps.file.api.serializers.file_serializers import FileDetalleSerializer
from apps.folder.api.serializers.treefolder_serializer import TreeFolderSerializer
from apps.folder.models import Folder, FolderInFolder
from rest_framework.response import Response
from rest_framework import status
from apps.folder.api.serializers.folder_serializer import (
    FolderBuscarSerializer,
    FolderSerializer,
    FolderDirecotorioListSerializer,
    FolderDeleteSerializer,
    FolderTrashListSerializer,
    FolderUpdatePrivateSerializer,
    FolderUpdateSerializer,
    FolderHistorySerializer
    )
from apps.file.models import File
from apps.users.authenticacion_mixings import Authentication
from rest_framework import viewsets
from django.utils.crypto import get_random_string  
from django.db.models import Q

#pendiente quitar
class FolderPrivateViewSet(Authentication,viewsets.GenericViewSet):
    serializer_class = FolderSerializer

    def get_queryset(self,pk = None):
        if pk is None:
            '''folderMaster = Folder.objects.filter(carpeta_hija__isnull =True,unidadArea_id = self.userFull.unidadArea_id).first()
            return self.serializer_class().Meta.model.objects.filter(scope = False,
                                                                    unidadArea_id = self.userFull.unidadArea_id,
                                                                    user_id =self.userFull.id,
                                                                    carpeta_hija__parent_folder__id = folderMaster.id)'''
            return self.serializer_class().Meta.model.objects.filter(scope = False,
                                                                    unidadArea_id = self.userFull.unidadArea_id,
                                                                    user_id =self.userFull.id,
                                                                    carpeta_hija__isnull =True)
        else:
            try:
                
                return self.serializer_class().Meta.model.objects.filter(slug = pk,unidadArea_id = self.userFull.unidadArea_id)
            except:
                return None
    def list(self,request):
        folders = FolderDirecotorioListSerializer(self.get_queryset(),many = True,context = {'userId':self.userFull.id,'userStaff': 6})
        return Response(folders.data,status = status.HTTP_200_OK)
    def retrieve(self,request,pk=None):
        folder = self.get_queryset(pk)
        print(folder)
        if folder:
            if folder.first().scope:
                return Response({'error':'La carpeta solicitada no es accesible'},status = status.HTTP_401_UNAUTHORIZED)
            if validarPrivado(folder.first(),self.userFull.id):
                return Response({'error':'La carpeta solicitada es privada'},status = status.HTTP_401_UNAUTHORIZED)
            createHistory(Folder,folder.first().id,"Obteniendo carpeta "+ folder.first().nombre,"o",self.userFull.id)
            folders = FolderDirecotorioListSerializer(folder,many = True,context = {'userId':self.userFull.id,'userStaff': 6})
            return Response(folders.data,status = status.HTTP_200_OK)
        return Response({'error':"El directorio no existe"},status = status.HTTP_400_BAD_REQUEST)   

class FolderViewSet(Authentication,viewsets.GenericViewSet):
    serializer_class = FolderSerializer

    def get_queryset(self,pk = None):
        if pk is None:
            #return self.serializer_class().Meta.model.objects.filter(user__is_superuser = True,carpeta_hija__isnull =True,unidadArea_id = self.userFull.unidadArea_id)
            if self.userFull.is_staff < 3:
                return self.serializer_class().Meta.model.objects.filter(Q(scope = False,
                                                                        unidadArea_id = self.userFull.unidadArea_id,
                                                                        user_id =self.userFull.id,
                                                                        carpeta_hija__isnull =True,eliminado = False)|
                                                                        Q(user__is_superuser = True,
                                                                        carpeta_hija__isnull =True,
                                                                        unidadArea_id = self.userFull.unidadArea_id,eliminado = False)).distinct()
            elif self.userFull.is_staff > 2 and self.userFull.is_staff < 5:
                #listar con todas las unidades privadas de los usuario
                #return self.serializer_class().Meta.model.objects.filter(user__is_superuser = True,carpeta_hija__isnull =True,
                #                                                        unidadArea_id = self.userFull.unidadArea_id)
                #listar solo la unidad
                return self.serializer_class().Meta.model.objects.filter(user__is_superuser = True,carpeta_hija__isnull =True,
                                                                        unidadArea_id = self.userFull.unidadArea_id,eliminado = False)
            elif self.userFull.is_staff == 5:
                #listar con todas las unidades privadas de los usuario
                #return self.serializer_class().Meta.model.objects.filter(user__is_superuser = True,carpeta_hija__isnull =True,
                #                                                        unidadArea_id = self.userFull.unidadArea_id)
                #listar solo la unidad
                return self.serializer_class().Meta.model.objects.filter(user__is_superuser = True,carpeta_hija__isnull =True,eliminado = False)
        else:
            try:
                if self.userFull.is_staff == 5:
                    return self.serializer_class().Meta.model.objects.filter(slug = pk,eliminado = False)
                return self.serializer_class().Meta.model.objects.filter(slug = pk,unidadArea_id = self.userFull.unidadArea_id,eliminado = False)
            except:
                return None
    def list(self,request):

        folders = FolderDirecotorioListSerializer(self.get_queryset(),many = True,context = {'userId':self.userFull.id,'userStaff': self.userFull.is_staff})

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
            '''if not folder.first().scope:
                return Response({'error':'La carpeta solicitada no es accesible'},status = status.HTTP_401_UNAUTHORIZED)'''
            if self.userFull.is_staff < 3:
                if validarPrivado(folder.first(),self.userFull.id):
                    return Response({'error':'La carpeta solicitada es privada'},status = status.HTTP_401_UNAUTHORIZED)
            
            #print(folder.id)
            #create history
            createHistory(Folder,folder.first().id,"Obteniendo carpeta "+ folder.first().nombre,"o",self.userFull.id)
            folders = FolderDirecotorioListSerializer(folder,many = True,context = {'userId':self.userFull.id,'userStaff': self.userFull.is_staff})
            '''padrePrivate = obtenerRuta(folder.first().id,[folder.first().nombre],True,False,True,self.userFull.id)
            if not padrePrivate:
                if folder.first().scope == True:
                    return Response(folders.data,status = status.HTTP_200_OK)
                elif folder.first().scope == False :
                    if folder.first().user_id == self.userFull.id:
                        return Response(folders.data,status = status.HTTP_200_OK)
            return Response({'error':'La carpeta solicitada es privada'},status = status.HTTP_401_UNAUTHORIZED)'''
            return Response(folders.data,status = status.HTTP_200_OK)
        return Response({'error':"El directorio no existe"},status = status.HTTP_400_BAD_REQUEST)
    #pendiente quitar
    def create(self,request):
        #if self.userFull.is_superuser == 1 :
        folder_serializer = self.serializer_class(data = request.data)
        if folder_serializer.is_valid():
            folder_serializer.validated_data['slug'] = get_random_string(length=11)
            folder_serializer.validated_data['user_id'] = self.userFull.id
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

#pendiente quitar        
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
                return Response({'Error':'No permitido'},status = status.HTTP_401_UNAUTHORIZED)  
        else:
            return Response(folderSerializer.errors,status = status.HTTP_400_BAD_REQUEST)
class FolderQuitAPIView(Authentication,viewsets.GenericViewSet):
    serializer_class = FolderDeleteSerializer
    def get_queryset(self,pk = None):
        return self.get_serializer().Meta.model.objects.filter(slug = pk,scope = False,unidadArea_id = self.userFull.unidadArea_id, user_id =self.userFull.id).first()
    
    def retrieve(self,request,pk = None):
        folderResult = self.get_queryset(pk)
        if folderResult:
            if self.userFull.is_staff < 3:
                if validarPrivado(folderResult,self.userFull.id):
                    return Response({'error':'La carpeta solicitada es privada'},status = status.HTTP_401_UNAUTHORIZED)
                if folderResult.eliminado ==True:
                    setDestruirHijos(folderResult.slug)
                    folderDeleteResult = self.get_queryset(pk)
                    folderDeleteResult.delete()
                    return Response({'Mensaje':'Folder destruido correctamente'},status = status.HTTP_200_OK)
                folderMasterPrivate = Folder.objects.get(scope = False,
                                                        unidadArea_id = self.userFull.unidadArea_id,
                                                        user_id =self.userFull.id,
                                                        carpeta_hija__isnull =True,eliminado = False)
                setEliminarHijos(folderResult.slug)
                FolderInFolder.objects.filter(child_folder_id = folderResult.id).update(parent_folder_id = folderMasterPrivate.id)
                File.objects.filter(fileinfolder__parent_folder_id = folderResult.id).update(eliminado = True)                                        
                folderResult.eliminado = True
                folderResult.save()
                '''FolderTrash.objects.create(
                    folder_id = folderResult.id,
                    user_id = self.userFull.id
                )'''
                
                
                return Response({'Mensaje':'Folder eliminado correctamente'},status = status.HTTP_200_OK)
            return Response({'Error':'No permitido'},status = status.HTTP_401_UNAUTHORIZED)  
        return Response({'mensaje':'La carpeta no existe'},status = status.HTTP_400_BAD_REQUEST)
class FolderRestaurarAPIView(Authentication,viewsets.GenericViewSet):
    serializer_class = FolderDeleteSerializer
    def get_queryset(self,pk = None):
        return self.get_serializer().Meta.model.objects.filter(slug = pk,scope = False,eliminado = True,unidadArea_id = self.userFull.unidadArea_id, user_id =self.userFull.id).first()
    
    def retrieve(self,request,pk = None):
        folderResult = self.get_queryset(pk)
        if folderResult:
            if self.userFull.is_staff < 3:
                if validarPrivado(folderResult,self.userFull.id):
                    return Response({'error':'La carpeta solicitada es privada'},status = status.HTTP_401_UNAUTHORIZED)
                folderMasterPrivate = Folder.objects.get(scope = False,
                                                        unidadArea_id = self.userFull.unidadArea_id,
                                                        user_id =self.userFull.id,
                                                        carpeta_hija__isnull =True,eliminado = False)
                setEliminarHijos(folderResult.slug,False)
                FolderInFolder.objects.filter(child_folder_id = folderResult.id).update(parent_folder_id = folderMasterPrivate.id)
                File.objects.filter(fileinfolder__parent_folder_id = folderResult.id).update(eliminado = False)                                        
                folderResult.eliminado = False
                folderResult.save()
                '''FolderTrash.objects.create(
                    folder_id = folderResult.id,
                    user_id = self.userFull.id
                )'''
                
                
                return Response({'Mensaje':'Folder restaurado en la carpeta privada correctamente'},status = status.HTTP_200_OK)
            return Response({'Error':'No permitido'},status = status.HTTP_401_UNAUTHORIZED)  
        return Response({'mensaje':'La carpeta no existe'},status = status.HTTP_400_BAD_REQUEST)
class FolderTrashAPIView(Authentication,viewsets.GenericViewSet):
    serializer_class = FolderTrashListSerializer  
    def get_queryset(self,pk = None):
        if pk is not None:
            
            return self.get_serializer().Meta.model.objects.filter(slug = pk,eliminado = True,unidadArea_id = self.userFull.unidadArea_id,user_id = self.userFull.id).first()
        folderMasterPrivate = Folder.objects.get(scope = False,
                                                        unidadArea_id = self.userFull.unidadArea_id,
                                                        user_id =self.userFull.id,
                                                        carpeta_hija__isnull =True,eliminado = False)
        return self.get_serializer().Meta.model.objects.filter(carpeta_hija__parent_folder_id = folderMasterPrivate.id,eliminado = True,unidadArea_id = self.userFull.unidadArea_id,user_id = self.userFull.id)
    def list(self,request):
        if self.userFull.is_staff < 3:
            folderMasterPrivate = Folder.objects.get(scope = False,
                                                        unidadArea_id = self.userFull.unidadArea_id,
                                                        user_id =self.userFull.id,
                                                        carpeta_hija__isnull =True,eliminado = False)
            folders = self.get_serializer(self.get_queryset(),many = True,context = {'userId':self.userFull.id,'userStaff': self.userFull.is_staff})

            fileSerializer = FileDetalleSerializer(File.objects.filter(fileinfolder__parent_folder_id = folderMasterPrivate.id,
                                                            eliminado = True,
                                                            user_id = self.userFull.id,
                                                            unidadArea_id = self.userFull.unidadArea_id),many = True)
            arbol = TreeFolderSerializer(self.get_queryset(),many = True)
            #return Response(folders.data,status = status.HTTP_200_OK)
            return Response({'nombre':'Papelera de '+ self.userFull.name,
                            'subDirectorios':folders.data,
                            'files':fileSerializer.data,
                            'treefolders':arbol.data },status = status.HTTP_200_OK)
        return Response({'error':'No permitido'},status = status.HTTP_400_BAD_REQUEST)
    def retrieve(self,request,pk):
        if self.userFull.is_staff < 3:
            folder = self.get_queryset(pk)
            if folder:
                if validarPrivado(folder,self.userFull.id):
                    return Response({'error':'La carpeta solicitada es privada'},status = status.HTTP_401_UNAUTHORIZED)
                if folder.eliminado == False:
                    return Response({'error':'La carpeta solicitada no esta eliminado'},status = status.HTTP_401_UNAUTHORIZED)
                folderSerializer = self.get_serializer(folder,context = {'userId':self.userFull.id,'userStaff': self.userFull.is_staff})
                return Response(folderSerializer.data,status = status.HTTP_200_OK)
            return Response({'mensaje':'La carpeta no existe'},status = status.HTTP_400_BAD_REQUEST)
        return Response({'error':'No permitido'},status = status.HTTP_400_BAD_REQUEST)
class FolderUpdateAPIView(Authentication,viewsets.GenericViewSet):
    serializer_class = FolderUpdateSerializer
    def get_queryset(self,pk = None):
        return self.get_serializer().Meta.model.objects.filter(slug = pk,eliminado = False).first()
    def update(self,request,pk = None):
        folderResult = self.get_queryset(pk)
        
        
        '''padrePrivate = obtenerRuta(folderResult.id,[folderResult.nombre],True,False,True,self.userFull.id)
        if padrePrivate:
            return Response({'error':'La carpeta es privada'},status = status.HTTP_401_UNAUTHORIZED)
        elif folderResult.scope == False:
            if not(folderResult.user_id == self.userFull.id):
                return Response({'error':'La carpeta es privada'},status = status.HTTP_401_UNAUTHORIZED)'''
        if folderResult:
            if not folderResult.scope:
                return Response({'error':'No puede modificar esta carpeta'},status = status.HTTP_401_UNAUTHORIZED)
            if validarPrivado(folderResult,self.userFull.id):
                return Response({'error':'La carpeta solicitada es privada'},status = status.HTTP_401_UNAUTHORIZED)
            folderUpdateSerializer = self.get_serializer(self.get_queryset(pk),data = request.data)
            if folderUpdateSerializer.is_valid():
                #setPublicHijos(folderResult.slug)
                '''if bool(folderUpdateSerializer.validated_data['scope']) == False:
                    folderUpdateSerializer.validated_data['user_id'] = self.userFull.id'''
                folder = folderUpdateSerializer.save()
                #set history subfolder
                setHistory(folder,'datos del folder actualizado',self.userFull.id)
                return Response({'Mensaje':'Folder actualizado correctamente'},status = status.HTTP_200_OK)
            else:
                return Response(folderUpdateSerializer.errors,status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'Error':'El folder no existe'},status = status.HTTP_400_BAD_REQUEST)
class FolderUpdatePrivateAPIView(Authentication,viewsets.GenericViewSet):
    serializer_class = FolderUpdatePrivateSerializer
    def get_queryset(self,pk = None):
        return self.get_serializer().Meta.model.objects.filter(slug = pk,eliminado = False).first()
    def update(self,request,pk = None):
        folderResult = self.get_queryset(pk)
        if folderResult:
            
            if folderResult.scope:
                return Response({'error':'No puede modificar esta carpeta'},status = status.HTTP_401_UNAUTHORIZED)
            if validarPrivado(folderResult,self.userFull.id):
                return Response({'error':'La carpeta solicitada es privada'},status = status.HTTP_401_UNAUTHORIZED)
            folderGestion = Folder.objects.filter(carpeta_hija__isnull =True,unidadArea_id = self.userFull.unidadArea_id).first()
            folderUpdateSerializer = self.get_serializer(self.get_queryset(pk),data = request.data)
            if folderUpdateSerializer.is_valid():
                if bool(folderUpdateSerializer.validated_data['scope']) == True:
                    #folderUpdateSerializer.validated_data['user_id'] = self.userFull.id
                    folderUpdateSerializer.validated_data['user_id'] = self.userFull.id
                    FolderInFolder.objects.filter(child_folder__slug = pk).update(parent_folder_id = folderGestion.id)
                    File.objects.filter(fileinfolder__parent_folder__slug = pk).update(scope = True)
                    setPublicHijos(folderResult.slug)
                    createHistory(Folder,folderResult.id,"Cambiando a publico "+ folderResult.nombre,"P",self.userFull.id)
                folder = folderUpdateSerializer.save()
                #set history subfolder
                setHistory(folder,'datos del folder actualizado',self.userFull.id)
                return Response({'Mensaje':'Folder actualizado correctamente'},status = status.HTTP_200_OK)
            else:
                return Response(folderUpdateSerializer.errors,status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'Error':'El folder no existe'},status = status.HTTP_400_BAD_REQUEST)
#falta validar privado
class FolderHistoryAPIView(Authentication,viewsets.GenericViewSet):
    serializer_class = FolderHistorySerializer
    def get_queryset(self,pk=None):
        if pk is not None:
            return Folder.historical.filter(id = pk,history_user_id=self.userFull.id)
        return Folder.historical.filter(history_user_id=self.userFull.id)
    def list(self,request):
        historyFolder = self.get_queryset()
        folderHistorialSerializer = self.get_serializer(historyFolder,many = True)
        return Response(folderHistorialSerializer.data, status = status.HTTP_200_OK)
    def retrieve(self,request,pk = None):
        folderResult = Folder.objects.get(slug = pk)
        if folderResult:
            if validarPrivado(folderResult.first(),self.userFull.id):
                return Response({'error':'La carpeta solicitada es privada'},status = status.HTTP_401_UNAUTHORIZED)
            historyFolder = self.get_queryset(folderResult.first().id)
            folderHistorialSerializer = self.get_serializer(historyFolder,many = True)
            return Response(folderHistorialSerializer.data, status = status.HTTP_200_OK)
        return Response({'Error':'El folder no existe'},status = status.HTTP_400_BAD_REQUEST)
class FolderBuscarAPIView(Authentication,viewsets.GenericViewSet):
    serializer_class = FolderBuscarSerializer
    def get_queryset(self, buscar):
        #return self.serializer_class().Meta.model.objects.filter(Q(nombre__icontains = buscar),carpeta_hija__isnull =True,unidadArea_id = self.userFull.unidadArea_id).distinct()
        if self.userFull.is_staff < 3:
            return self.serializer_class().Meta.model.objects.filter(Q(nombre__icontains = buscar,scope = False,user_id = self.userFull.id,eliminado = False)|
                                                                    Q(nombre__icontains = buscar,scope = True,eliminado = False),
                                                                    unidadArea_id = self.userFull.unidadArea_id,eliminado = False).distinct()
        #return self.serializer_class().Meta.model.objects.filter(nombre__icontains = buscar,unidadArea_id = self.userFull.unidadArea_id,eliminado = False).distinct()
        return self.serializer_class().Meta.model.objects.filter(nombre__icontains = buscar,eliminado = False,scope=True).distinct()
    def create(self,request):
        folder_serializer = self.get_serializer(data = request.data)
        if folder_serializer.is_valid():
            folders = FolderDirecotorioListSerializer(self.get_queryset(request.data['buscar']),many = True,context = {'userId':self.userFull.id,'userStaff': self.userFull.is_staff})
            return Response(folders.data,status = status.HTTP_200_OK)
        else:
            return Response(folder_serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        
    




